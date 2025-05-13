USE SISTORE2TEST;

WITH RentDuration AS (
	SELECT 
		t.TenantID AS TenantID, 
		r.MoveInDate AS MoveInDate,
		r.MoveOutDate AS MoveOutDate,
		r.RentedRoom AS RoomNumber,
		TIMESTAMPDIFF(MONTH, r.MoveInDate, r.MoveOutDate) AS Duration
	FROM Tenant t
	LEFT JOIN Rents r ON t.TenantID = r.RentingTenant
),

MoveStatus AS (
	SELECT
		t.TenantID AS TenantID,
		CASE
			WHEN rd.MoveOutDate IS NOT NULL AND rd.MoveOutDate <= CURRENT_DATE() THEN "Moved Out"
			WHEN rd.MoveOutDate > CURRENT_DATE() THEN "Active"
			ELSE "Moved Out"
		END AS MoveStatus
	FROM Tenant t
	LEFT JOIN RentDuration rd ON t.TenantID = rd.TenantID
),

PaidAmount AS (
	SELECT 
		p.PayingTenant AS TenantID, 
		SUM(p.PaymentAmount) AS PaidAmount
	FROM Pays p
	GROUP BY p.PayingTenant
),

RemainingDue AS (
	SELECT 
		rd.TenantID AS TenantID,
		((COALESCE(r.Price, 0) * COALESCE(rd.Duration, 0)) - COALESCE(pa.PaidAmount, 0)) AS RemainingDue
	FROM RentDuration rd
	LEFT JOIN PaidAmount pa ON rd.TenantID = pa.TenantID
	LEFT JOIN Room r ON r.RoomNumber = rd.RoomNumber
),

PaymentStatus AS (
	SELECT 
		t.TenantID AS TenantID,
		CASE
			WHEN pa.PaidAmount IS NULL THEN "Pending"
            WHEN COALESCE(pa.PaidAmount, 0) < COALESCE(red.RemainingDue, 0) AND CURRENT_DATE() > rd.MoveOutDate THEN "Overdue"
			WHEN COALESCE(pa.PaidAmount, 0) >= COALESCE(red.RemainingDue, 0) THEN "Paid"
			ELSE "Pending"
		END AS PaymentStatus
	FROM Tenant t
	LEFT JOIN RentDuration rd ON t.TenantID = rd.TenantID
	LEFT JOIN RemainingDue red ON t.TenantID = red.TenantID
	LEFT JOIN PaidAmount pa ON t.TenantID = pa.TenantID
)

SELECT 
	Tenant.*, 
	MoveStatus.MoveStatus, 
	PaymentStatus.PaymentStatus, 
	EmergencyContact.PhoneNumber
FROM Tenant 
LEFT JOIN EmergencyContact ON Tenant.TenantID = EmergencyContact.EMTenantID
LEFT JOIN MoveStatus ON Tenant.TenantID = MoveStatus.TenantID
LEFT JOIN PaymentStatus ON Tenant.TenantID = PaymentStatus.TenantID;
