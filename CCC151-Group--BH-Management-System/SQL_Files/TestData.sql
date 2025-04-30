CREATE DATABASE IF NOT EXISTS SISTORE;
USE SISTORE;

CREATE TABLE IF NOT EXISTS Room (
    RoomNumber INTEGER PRIMARY KEY,
    Price DECIMAL(7,2) NOT NULL,
    TenantSex VARCHAR(6) NOT NULL CHECK (TenantSex IN ('Male', 'Female')),
    MaximumCapacity INTEGER NOT NULL,
    NoOfOccupants INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS  Tenant (
    TenantID VARCHAR(9) PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    FirstName VARCHAR(128) NOT NULL,
    MiddleName VARCHAR(128),
    LastName VARCHAR(128) NOT NULL,
    Sex VARCHAR(6) NOT NULL CHECK (Sex IN ('Male', 'Female')),
    PhoneNumber VARCHAR(100) NOT NULL,
    RoomNumber INT NOT NULL,
    FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)
		ON UPDATE CASCADE
		ON DELETE RESTRICT,
    CONSTRAINT tenant_fullname UNIQUE (FirstName, LastName)
);

CREATE TABLE IF NOT EXISTS  Rents (
    RentedRoom INTEGER NOT NULL,
    RentingTenant VARCHAR(9) NOT NULL,
    MoveStatus VARCHAR(50) NOT NULL CHECK (MoveStatus IN ('Active', 'Moved Out')),
    MoveInDate DATE NOT NULL,
    MoveOutDate DATE,
    FOREIGN KEY (RentedRoom) REFERENCES Room(RoomNumber)		-- check
		ON DELETE RESTRICT
	            ON UPDATE CASCADE,    
     FOREIGN KEY (RentingTenant) REFERENCES Tenant(TenantID) 	-- check
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
      CONSTRAINT StartDateLimit CHECK (MoveOutDate IS NULL OR MoveInDate <= MoveOutDate)

);

CREATE TABLE IF NOT EXISTS  Pays (
	PayID INT AUTO_INCREMENT PRIMARY KEY,	
	PaymentAmount DECIMAL(7,2) NOT NULL,		
	PaymentDate DATE NOT NULL,			
	PaymentStatus VARCHAR(10) NOT NULL,		
	PayingTenant VARCHAR(9) NOT NULL,		
	PaidRoom INT NOT NULL,				

	FOREIGN KEY (PayingTenant) REFERENCES Tenant(TenantID)		-- check
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (PaidRoom) REFERENCES Room(RoomNumber)		-- check
		ON DELETE RESTRICT
		ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS  EmergencyContact (
    ContactID VARCHAR(9) PRIMARY KEY,
    FirstName VARCHAR(128) NOT NULL,
    MiddleName VARCHAR(128),
    LastName VARCHAR(128) NOT NULL,
    Relationship VARCHAR(128) NOT NULL,
    PhoneNumber VARCHAR(100) NOT NULL,
    EMTenantID VARCHAR(9) NOT NULL,
    FOREIGN KEY (EMTenantID) REFERENCES Tenant(TenantID)
    	ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- Male
INSERT INTO Room (RoomNumber, Price, TenantSex, MaximumCapacity, NoOfOccupants) VALUES
(301, 2000.00, 'Male', 2, 1),
(302, 2000.00, 'Male', 2, 1),
(303, 2000.00, 'Male', 2, 1),
(304, 2000.00, 'Male', 2, 1),
(305, 2000.00, 'Male', 2, 1),
(306, 2000.00, 'Male', 2, 1),
(307, 2000.00, 'Male', 2, 1),
(308, 2000.00, 'Male', 2, 1),
(309, 2000.00, 'Male', 2, 1),
(310, 2000.00, 'Male', 2, 1);

-- Female
INSERT INTO Room (RoomNumber, Price, TenantSex, MaximumCapacity, NoOfOccupants) VALUES
(201, 2000.00, 'Female', 2, 1),
(202, 2000.00, 'Female', 2, 1),
(203, 2000.00, 'Female', 2, 1),
(204, 2000.00, 'Female', 2, 1),
(205, 2000.00, 'Female', 2, 1),
(206, 2000.00, 'Female', 2, 1),
(207, 2000.00, 'Female', 2, 1),
(208, 2000.00, 'Female', 2, 1),
(209, 2000.00, 'Female', 2, 1),
(210, 2000.00, 'Female', 2, 1);


INSERT INTO Tenant (TenantID, Email, FirstName, MiddleName, LastName, Sex, PhoneNumber, RoomNumber) VALUES
('2025-4321', 'amanda.johnson@email.com', 'Amanda', 'Lee', 'Johnson', 'Female', '9171234567', 201),
('2025-4322', 'brandon.smith@email.com', 'Brandon', 'Allen', 'Smith', 'Male', '9181234568', 301),
('2025-4323', 'carla.garcia@email.com', 'Carla', 'Anne', 'Garcia', 'Female', '9191234569', 202),
('2025-4324', 'daniel.brown@email.com', 'Daniel', 'James', 'Brown', 'Male', '9201234570', 302),
('2025-4325', 'emma.davis@email.com', 'Emma', 'Lynn', 'Davis', 'Female', '9211234571', 203),
('2025-4326', 'fiona.wilson@email.com', 'Fiona', 'Marie', 'Wilson', 'Female', '9221234572', 204),
('2025-4327', 'gabriel.martinez@email.com', 'Gabriel', 'Jay', 'Martinez', 'Male', '9231234573', 303),
('2025-4328', 'hannah.anderson@email.com', 'Hannah', 'Rae', 'Anderson', 'Female', '9241234574', 205),
('2025-4329', 'ian.thomas@email.com', 'Ian', 'Neil', 'Thomas', 'Male', '9251234575', 304),
('2025-4330', 'julia.taylor@email.com', 'Julia', 'June', 'Taylor', 'Female', '9261234576', 206),
('2025-4331', 'kevin.moore@email.com', 'Kevin', 'Scott', 'Moore', 'Male', '9271234577', 305),
('2025-4332', 'lily.jackson@email.com', 'Lily', 'Ann', 'Jackson', 'Female', '9281234578', 207),
('2025-4333', 'mason.white@email.com', 'Mason', 'Luke', 'White', 'Male', '9291234579', 306),
('2025-4334', 'natalie.harris@email.com', 'Natalie', 'Elle', 'Harris', 'Female', '9301234580', 208),
('2025-4335', 'owen.martin@email.com', 'Owen', 'Chase', 'Martin', 'Male', '9311234581', 307),
('2025-4336', 'paige.thompson@email.com', 'Paige', 'Sky', 'Thompson', 'Female', '9321234582', 209),
('2025-4337', 'quentin.garcia@email.com', 'Quentin', 'Jude', 'Garcia', 'Male', '9331234583', 308),
('2025-4338', 'riley.martinez@email.com', 'Riley', 'Faith', 'Martinez', 'Female', '9341234584', 210),
('2025-4339', 'sean.robinson@email.com', 'Sean', 'Dean', 'Robinson', 'Male', '9351234585', 309),
('2025-4340', 'tesson.clark@email.com', 'Tesson', 'Everest', 'Clark', 'Male', '9361234586', 310);

INSERT INTO Rents (RentedRoom, RentingTenant, MoveStatus, MoveInDate, MoveOutDate) VALUES
-- Male tenants
(301, '2025-4322', 'Active', '2025-01-15', '2025-12-15'),
(302, '2025-4324', 'Active', '2025-02-01', '2025-11-30'),
(303, '2025-4327', 'Active', '2025-01-10', '2025-10-10'),
(304, '2025-4329', 'Active', '2025-03-05', '2026-03-04'),
(305, '2025-4331', 'Active', '2025-02-20', '2025-12-20'),
(306, '2025-4333', 'Active', '2025-01-25', '2025-10-25'),
(307, '2025-4335', 'Active', '2025-02-15', '2025-11-15'),
(308, '2025-4337', 'Active', '2025-03-01', '2026-02-28'),
(309, '2025-4339', 'Active', '2025-01-05', '2025-10-05'),
(310, '2025-4340', 'Active', '2025-02-10', '2025-11-10'),
-- Female tenants
(201, '2025-4321', 'Active', '2025-01-10', '2025-12-10'),
(202, '2025-4323', 'Active', '2025-01-20', '2025-11-20'),
(203, '2025-4325', 'Active', '2025-02-01', '2025-12-01'),
(204, '2025-4326', 'Active', '2025-01-15', '2025-11-15'),
(205, '2025-4328', 'Active', '2025-03-05', '2026-03-05'),
(206, '2025-4330', 'Active', '2025-02-20', '2025-12-20'),
(207, '2025-4332', 'Active', '2025-01-25', '2025-10-25'),
(208, '2025-4334', 'Active', '2025-03-01', '2026-02-28'),
(209, '2025-4336', 'Active', '2025-01-05', '2025-10-05'),
(210, '2025-4338', 'Active', '2025-02-10', '2025-11-10');


INSERT INTO Pays (PaidRoom, PayingTenant, PaymentStatus, PaymentAmount, PaymentDate) VALUES
-- Male tenants
(301, '2025-4322', 'Paid', 2000.00, '2025-04-01'),
(302, '2025-4324', 'Pending', 2000.00, '2025-04-02'),
(303, '2025-4327', 'Paid', 2000.00, '2025-04-03'),
(304, '2025-4329', 'Overdue', 2000.00, '2025-03-30'),
(305, '2025-4331', 'Paid', 2000.00, '2025-04-01'),
(306, '2025-4333', 'Pending', 2000.00, '2025-04-04'),
(307, '2025-4335', 'Paid', 2000.00, '2025-04-05'),
(308, '2025-4337', 'Overdue', 2000.00, '2025-03-31'),
(309, '2025-4339', 'Paid', 2000.00, '2025-04-02'),
(310, '2025-4340', 'Pending', 2000.00, '2025-04-06'),
-- Female tenants
(201, '2025-4321', 'Paid', 2000.00, '2025-04-01'),
(202, '2025-4323', 'Pending', 2000.00, '2025-04-02'),
(203, '2025-4325', 'Paid', 2000.00, '2025-04-03'),
(204, '2025-4326', 'Overdue', 2000.00, '2025-03-30'),
(205, '2025-4328', 'Paid', 2000.00, '2025-04-01'),
(206, '2025-4330', 'Pending', 2000.00, '2025-04-04'),
(207, '2025-4332', 'Paid', 2000.00, '2025-04-05'),
(208, '2025-4334', 'Overdue', 2000.00, '2025-03-31'),
(209, '2025-4336', 'Paid', 2000.00, '2025-04-02'),
(210, '2025-4338', 'Pending', 2000.00, '2025-04-06');

INSERT INTO EmergencyContact (ContactID, FirstName, MiddleName, LastName, Relationship, PhoneNumber, EMTenantID) VALUES
('EC2025001', 'Michael', 'James', 'Johnson', 'Father', '9179876543', '2025-4321'),
('EC2025002', 'Lisa', 'Marie', 'Smith', 'Mother', '9189876544', '2025-4322'),
('EC2025003', 'Robert', 'Allen', 'Garcia', 'Brother', '9199876545', '2025-4323'),
('EC2025004', 'Karen', NULL, 'Brown', 'Aunt', '9209876546', '2025-4324'),
('EC2025005', 'David', 'Lee', 'Davis', 'Uncle', '9219876547', '2025-4325'),
('EC2025006', 'Jessica', 'Ann', 'Wilson', 'Sister', '9229876548', '2025-4326'),
('EC2025007', 'Thomas', 'Jay', 'Martinez', 'Father', '9239876549', '2025-4327'),
('EC2025008', 'Nancy', 'Rae', 'Anderson', 'Mother', '9249876550', '2025-4328'),
('EC2025009', 'Charles', 'Neil', 'Thomas', 'Brother', '9259876551', '2025-4329'),
('EC2025010', 'Barbara', 'June', 'Taylor', 'Grandmother', '9269876552', '2025-4330');

SELECT Tenant.TenantID, Tenant.Email, Tenant.FirstName, Tenant.MiddleName, Tenant.LastName, Tenant.Sex, Tenant.PhoneNumber, Tenant.RoomNumber, EmergencyContact.PhoneNumber
FROM Tenant LEFT JOIN EmergencyContact 
ON Tenant.TenantID = EmergencyContact.EMTenantID;



