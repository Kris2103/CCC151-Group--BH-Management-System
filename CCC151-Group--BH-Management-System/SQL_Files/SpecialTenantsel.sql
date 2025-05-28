WITH  LatestRent AS (
                            SELECT
                                rt.RentID,
                                rt.RentingTenant AS TenantID,
                                rt.MoveInDate,
                                rt.MoveOutDate,
                                rt.RentedRoom AS RoomNumber,
                                r.Price
                            FROM Rents rt
                            LEFT JOIN Room r ON r.RoomNumber = rt.RentedRoom
                            WHERE rt.RentID = (
                                SELECT MAX(inner_rt.RentID)
                                FROM Rents inner_rt
                                WHERE inner_rt.RentingTenant = rt.RentingTenant
                            )
                        ) ,  MonthlyPaidRoom AS (
                            SELECT DISTINCT
                                p.PaidRoom AS RoomNumber,
                                DATE_FORMAT(p.PaymentDate, '%Y-%m-01') AS PaymentMonthDate,
                                SUM(p.PaymentAmount) AS TotalPaid
                            FROM Pays p
                            GROUP BY p.PaidRoom, DATE_FORMAT(p.PaymentDate, '%Y-%m-01')
                        ) ,  WholePaidRoomTenant AS (
                            SELECT
                                r.RentID,
                                SUM(mpr.TotalPaid) AS WholePaid
                            FROM Rents r
                            LEFT JOIN MonthlyPaidRoom mpr
                                ON r.RentedRoom = mpr.RoomNumber
                                AND DATE(mpr.PaymentMonthDate) BETWEEN DATE_FORMAT(r.MoveInDate, '%Y-%m-01') AND DATE_FORMAT(r.MoveOutDate, '%Y-%m-01')
                            GROUP BY r.RentID
                        ) ,  RentDuration AS (
                            SELECT
                                t.TenantID,
                                r.MoveInDate,
                                r.MoveOutDate,
                                r.RentedRoom AS RoomNumber,
                                TIMESTAMPDIFF(MONTH, r.MoveInDate, r.MoveOutDate) AS Duration,
                                CASE
                                    WHEN (CURRENT_DATE() BETWEEN r.MoveInDate AND r.MoveOutDate) AND t.RoomNumber = r.RentedRoom THEN "Active"
                                    ELSE "Moved Out"
                                END AS MoveStatus
                            FROM Rents r
                            LEFT JOIN Tenant t ON t.TenantID = r.RentingTenant
                        ) ,  PaidAmount AS (
                            SELECT
                                p.PayingTenant AS TenantID,
                                p.PaidRoom AS RoomNumber,
                                SUM(p.PaymentAmount) AS PaidAmount,
                                MAX(p.PaymentDate) AS LastPaymentDate,
                                COALESCE(SUM(CASE
                                                WHEN MONTH(p.PaymentDate) = MONTH(CURRENT_DATE())
                                                    AND YEAR(p.PaymentDate) = YEAR(CURRENT_DATE())
                                                THEN p.PaymentAmount
                                                ELSE 0
                                            END), 0) AS PaidThisMonth
                            FROM Pays p
                            LEFT JOIN LatestRent r
                                ON r.TenantID = p.PayingTenant
                                AND p.PaymentDate BETWEEN r.MoveInDate AND r.MoveOutDate
                            GROUP BY p.PayingTenant, p.PaidRoom
                        ) ,  RemainingDue AS (
                            SELECT
                                rm.Price,
                                r.RentID,
                                r.RentingTenant AS TenantID,
                                (COALESCE(rm.Price, 0) * COALESCE(TIMESTAMPDIFF(MONTH, r.MoveInDate, r.MoveOutDate), 0))
                                - COALESCE(wpa.WholePaid, 0) AS RemainingDue
                            FROM Rents r
                            LEFT JOIN Room rm ON r.RentedRoom = rm.RoomNumber
                            LEFT JOIN WholePaidRoomTenant wpa ON r.RentID = wpa.RentID
                        ) ,  PaymentStatus AS (
                            SELECT
                                t.TenantID AS TenantID,
                                CASE
                                    WHEN mpr.TotalPaid IS NULL AND red.RemainingDue IS NULL THEN "No Payments"
                                    WHEN COALESCE(red.RemainingDue, 0) <= 0 THEN "Paid"
                                    WHEN COALESCE(red.RemainingDue, 0) > 0 AND CURRENT_DATE() > rd.MoveOutDate THEN "Overdue"
                                    WHEN COALESCE(mpr.TotalPaid, 0) < (COALESCE(red.Price, 0) * TIMESTAMPDIFF(
                                                                                                                MONTH,
                                                                                                                rd.MoveInDate,
                                                                                                                CURRENT_DATE()
                                                                                                            )
                                                                    )THEN "Overdue"
                                    ELSE "Pending"
                                END AS PaymentStatus,
                                COALESCE(rd.Duration, 0) - FLOOR(COALESCE(mpr.TotalPaid, 0) / COALESCE(red.Price, 1)) AS UnpaidMonths
                            FROM Tenant t
                            LEFT JOIN RentDuration rd ON t.TenantID = rd.TenantID
                            LEFT JOIN RemainingDue red ON t.TenantID = red.TenantID
                            LEFT JOIN MonthlyPaidRoom mpr ON t.RoomNumber = mpr.RoomNumber
                            ) SELECT DISTINCT Tenant.FirstName, Tenant.MiddleName, Tenant.LastName, Tenant.Sex, Tenant.PhoneNumber, Tenant.Email, RentDuration.MoveStatus, RentDuration.RoomNumber, PaymentStatus.PaymentStatus, RemainingDue.RemainingDue, PaidAmount.PaidAmount, EmergencyContact.PhoneNumber FROM Tenant  LEFT JOIN Pays
                                                    ON Tenant.TenantID = Pays.PayingTenant
                                                LEFT JOIN LatestRent
                                                    ON Tenant.TenantID = LatestRent.TenantID
                                                LEFT JOIN RentDuration
                                                    ON RentDuration.TenantID = Tenant.TenantID
                                                LEFT JOIN PaidAmount
                                                    ON PaidAmount.TenantID = Tenant.TenantID
                                                LEFT JOIN RemainingDue
                                                    ON RemainingDue.TenantID = Tenant.TenantID
                                                LEFT JOIN PaymentStatus
                                                    ON PaymentStatus.TenantID = Tenant.TenantID
                                                LEFT JOIN EmergencyContact
                                                    ON EmergencyContact.EMTenantID = Tenant.TenantID
                                            WHERE Tenant.TenantID LIKE %s