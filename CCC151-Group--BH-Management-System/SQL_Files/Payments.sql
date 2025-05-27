USE SISTORE3TEST;

WITH MonthlyPaidRoom AS (
    SELECT 
        p.PaidRoom AS RoomNumber,
        YEAR(p.PaymentDate) AS PaymentYear,
        MONTH(p.PaymentDate) AS PaymentMonth,
        SUM(p.PaymentAmount) AS TotalPaid
    FROM Pays p
    GROUP BY p.PaidRoom, YEAR(p.PaymentDate), MONTH(p.PaymentDate)
),

LatestRent AS (
    SELECT 
        rt.RentID AS RentID,
        rt.RentingTenant AS TenantID,
        rt.MoveInDate AS MoveInDate,
        rt.MoveOutDate AS MoveOutDate,
        rt.RentedRoom AS RoomNumber,
        r.Price AS Price
    FROM Rents rt
    LEFT JOIN Room r ON r.RoomNumber = rt.RentedRoom
    WHERE rt.RentID = (
        SELECT MAX(inner_rt.RentID)
        FROM Rents inner_rt
        WHERE inner_rt.RentingTenant = rt.RentingTenant
    )
),

RentDuration AS (
    SELECT 
        t.TenantID AS TenantID,
        r.MoveInDate AS MoveInDate,
        r.MoveOutDate AS MoveOutDate,
        r.RentedRoom AS RoomNumber,
        TIMESTAMPDIFF(MONTH, r.MoveInDate, r.MoveOutDate) AS Duration,
        CASE
            WHEN (CURRENT_DATE() BETWEEN r.MoveInDate AND r.MoveOutDate) AND t.RoomNumber = r.RentedRoom THEN 'Active'
            ELSE 'Moved Out'
        END AS MoveStatus
    FROM Rents r
    LEFT JOIN Tenant t ON t.TenantID = r.RentingTenant
),

TotalDueRoom AS (
    SELECT 
        r.MoveInDate AS MoveInDate,
        r.MoveOutDate AS MoveOutDate,
        r.RentedRoom AS RoomNumber,
        SUM(mpr.TotalPaid) AS TotalPaidinRD
    FROM Rents r
    LEFT JOIN MonthlyPaidRoom mpr 
        ON r.RentedRoom = mpr.RoomNumber
        AND (mpr.PaymentYear * 100 + mpr.PaymentMonth) 
            BETWEEN (YEAR(r.MoveInDate) * 100 + MONTH(r.MoveInDate))
            AND (YEAR(r.MoveOutDate) * 100 + MONTH(r.MoveOutDate))
    GROUP BY r.RentedRoom, r.MoveInDate, r.MoveOutDate
),

RemainingDue AS (
    SELECT 
        rd.TenantID AS TenantID,
        r.Price AS Price,
        COALESCE(r.Price, 0) * COALESCE(rd.Duration, 0) AS TotalDue,
        (COALESCE(r.Price, 0) * COALESCE(rd.Duration, 0)) - COALESCE(tdr.TotalPaidinRD, 0) AS RemainingDue
    FROM RentDuration rd
    LEFT JOIN Room r ON r.RoomNumber = rd.RoomNumber
    LEFT JOIN TotalDueRoom tdr ON rd.RoomNumber = tdr.RoomNumber
)

SELECT DISTINCT
    p.*,
    rem.TotalDue,
    rem.RemainingDue
FROM Pays p
LEFT JOIN LatestRent r ON p.PayingTenant = r.TenantID
LEFT JOIN RentDuration rd ON p.PayingTenant = rd.TenantID
LEFT JOIN MonthlyPaidRoom mpr 
    ON p.PaidRoom = mpr.RoomNumber 
    AND YEAR(p.PaymentDate) = mpr.PaymentYear 
    AND MONTH(p.PaymentDate) = mpr.PaymentMonth
LEFT JOIN TotalDueRoom tdr ON p.PaidRoom = tdr.RoomNumber
LEFT JOIN RemainingDue rem ON p.PayingTenant = rem.TenantID;
