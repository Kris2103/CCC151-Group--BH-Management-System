CREATE DATABASE IF NOT EXISTS SISTORE3TEST;
USE SISTORE3TEST;

CREATE TABLE IF NOT EXISTS Room (
    RoomNumber      INTEGER       PRIMARY KEY,
    Price           DECIMAL(9,2)  NOT NULL,
    TenantSex       VARCHAR(6) 
                    CHECK (TenantSex IN ('Male', 'Female', NULL)),
    MaximumCapacity INTEGER       NOT NULL
                    DEFAULT 0
);
CREATE TABLE IF NOT EXISTS  Tenant (
    TenantID        VARCHAR(9)    PRIMARY KEY,
    Email           VARCHAR(255)  NOT NULL,
    FirstName       VARCHAR(128)  NOT NULL,
    MiddleName      VARCHAR(128),
    LastName        VARCHAR(128)  NOT NULL,
    Sex             VARCHAR(6)    NOT NULL 
                    CHECK (Sex IN ('Male', 'Female')),
    PhoneNumber     VARCHAR(100)  NOT NULL,
    RoomNumber      INTEGER,
    
    CONSTRAINT fk_tenantToRoom 
      FOREIGN KEY (RoomNumber) REFERENCES Room(RoomNumber)
        ON UPDATE CASCADE
        ON DELETE RESTRICT, 
    CONSTRAINT tenant_fullname 
      UNIQUE (FirstName, LastName),
    CONSTRAINT tenant_contact 
      UNIQUE (Email, PhoneNumber)
);

CREATE TABLE IF NOT EXISTS  Rents (
    RentID          INTEGER       PRIMARY KEY
                    AUTO_INCREMENT,
    RentingTenant   VARCHAR(9)    NOT NULL,
    RentedRoom      INTEGER       NOT NULL,
    MoveInDate      DATE          NOT NULL,
    MoveOutDate     DATE          NOT NULL,
    CONSTRAINT StartDateLimit 
      CHECK (MoveOutDate IS NULL OR MoveInDate <= MoveOutDate)
);

CREATE TABLE IF NOT EXISTS  Pays (
	PayID             INTEGER       PRIMARY KEY
                    AUTO_INCREMENT,	
  PayingTenant      VARCHAR(9)    NOT NULL,		
	PaidRoom          INTEGER       NOT NULL,
	PaymentAmount     DECIMAL(9,2)  NOT NULL,		
	PaymentDate       DATE          NOT NULL			
);

CREATE TABLE IF NOT EXISTS  EmergencyContact (
    ContactID       VARCHAR(9)    PRIMARY KEY,
    FirstName       VARCHAR(128)  NOT NULL,
    MiddleName      VARCHAR(128),
    LastName        VARCHAR(128)  NOT NULL,
    Relationship    VARCHAR(128)  NOT NULL,
    PhoneNumber     VARCHAR(100)  NOT NULL,
    EMTenantID      VARCHAR(9)    NOT NULL,

    CONSTRAINT fk_emToTenant
      FOREIGN KEY (EMTenantID) REFERENCES Tenant(TenantID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO Room (RoomNumber, Price, MaximumCapacity) VALUES

-- -- Male
-- (301, 2000.00, 'Male', 2),
-- (302, 2000.00, 'Male', 2),
-- (303, 2000.00, 'Male', 2),
-- (304, 2000.00, 'Male', 2),
-- (305, 2000.00, 'Male', 2),
-- (306, 2000.00, 'Male', 2),
-- (307, 2000.00, 'Male', 2),
-- (308, 2000.00, 'Male', 2),
-- (309, 2000.00, 'Male', 2),
-- (310, 2000.00, 'Male', 2),

-- -- Female
-- (201, 2000.00, 'Female', 2),
-- (202, 2000.00, 'Female', 2),
-- (203, 2000.00, 'Female', 2),
-- (204, 2000.00, 'Female', 2),
-- (205, 2000.00, 'Female', 2),
-- (206, 2000.00, 'Female', 2),
-- (207, 2000.00, 'Female', 2),
-- (208, 2000.00, 'Female', 2),
-- (209, 2000.00, 'Female', 2),
-- (210, 2000.00, 'Female', 2);

(301, 2000.00, 2),
(302, 2000.00, 2),
(303, 2000.00, 2),
(304, 2000.00, 2),
(305, 2000.00, 2),
(306, 2000.00, 2),
(307, 2000.00, 2),
(308, 2000.00, 2),
(309, 2000.00, 2),
(310, 2000.00, 2),

(201, 2000.00, 2),
(202, 2000.00, 2),
(203, 2000.00, 2),
(204, 2000.00, 2),
(205, 2000.00, 2),
(206, 2000.00, 2),
(207, 2000.00, 2),
(208, 2000.00, 2),
(209, 2000.00, 2),
(210, 2000.00, 2);

INSERT INTO Tenant (TenantID, Email, FirstName, MiddleName, LastName, Sex, PhoneNumber) VALUES
('2025-4321', 'amanda.johnson@email.com', 'Amanda', 'Lee', 'Johnson', 'Female', '9171234567'),
('2025-4322', 'brandon.smith@email.com', 'Brandon', 'Allen', 'Smith', 'Male', '9181234568'),
('2025-4323', 'carla.garcia@email.com', 'Carla', 'Anne', 'Garcia', 'Female', '9191234569'),
('2025-4324', 'daniel.brown@email.com', 'Daniel', 'James', 'Brown', 'Male', '9201234570'),
('2025-4325', 'emma.davis@email.com', 'Emma', 'Lynn', 'Davis', 'Female', '9211234571'),
('2025-4326', 'fiona.wilson@email.com', 'Fiona', 'Marie', 'Wilson', 'Female', '9221234572'),
('2025-4327', 'gabriel.martinez@email.com', 'Gabriel', 'Jay', 'Martinez', 'Male', '9231234573'),
('2025-4328', 'hannah.anderson@email.com', 'Hannah', 'Rae', 'Anderson', 'Female', '9241234574'),
('2025-4329', 'ian.thomas@email.com', 'Ian', 'Neil', 'Thomas', 'Male', '9251234575'),
('2025-4330', 'julia.taylor@email.com', 'Julia', 'June', 'Taylor', 'Female', '9261234576'),
('2025-4331', 'kevin.moore@email.com', 'Kevin', 'Scott', 'Moore', 'Male', '9271234577'),
('2025-4332', 'lily.jackson@email.com', 'Lily', 'Ann', 'Jackson', 'Female', '9281234578'),
('2025-4333', 'mason.white@email.com', 'Mason', 'Luke', 'White', 'Male', '9291234579'),
('2025-4334', 'natalie.harris@email.com', 'Natalie', 'Elle', 'Harris', 'Female', '9301234580'),
('2025-4335', 'owen.martin@email.com', 'Owen', 'Chase', 'Martin', 'Male', '9311234581'),
('2025-4336', 'paige.thompson@email.com', 'Paige', 'Sky', 'Thompson', 'Female', '9321234582'),
('2025-4337', 'quentin.garcia@email.com', 'Quentin', 'Jude', 'Garcia', 'Male', '9331234583'),
('2025-4338', 'riley.martinez@email.com', 'Riley', 'Faith', 'Martinez', 'Female', '9341234584'),
('2025-4339', 'sean.robinson@email.com', 'Sean', 'Dean', 'Robinson', 'Male', '9351234585'),
('2025-4340', 'tesson.clark@email.com', 'Tesson', 'Everest', 'Clark', 'Male', '9361234586');

-- INSERT INTO Rents (RentedRoom, RentingTenant, MoveInDate, MoveOutDate) VALUES
-- -- Male tenants
-- (301, '2025-4322', '2025-01-15', '2025-12-15'),
-- (302, '2025-4324', '2025-02-01', '2025-11-30'),
-- (303, '2025-4327', '2025-01-10', '2025-10-10'),
-- (304, '2025-4329', '2025-03-05', '2026-03-04'),
-- (305, '2025-4331', '2025-02-20', '2025-12-20'),
-- (306, '2025-4333', '2025-01-25', '2025-10-25'),
-- (307, '2025-4335', '2025-02-15', '2025-11-15'),
-- (308, '2025-4337', '2025-03-01', '2026-02-28'),
-- (309, '2025-4339', '2025-01-05', '2025-10-05'),
-- (310, '2025-4340', '2025-02-10', '2025-11-10'),
-- -- Female tenants
-- (201, '2025-4321', '2025-01-10', '2025-12-10'),
-- (202, '2025-4323', '2025-01-20', '2025-11-20'),
-- (203, '2025-4325', '2025-02-01', '2025-12-01'),
-- (204, '2025-4326', '2025-01-15', '2025-11-15'),
-- (205, '2025-4328', '2025-03-05', '2026-03-05'),
-- (206, '2025-4330', '2025-02-20', '2025-12-20'),
-- (207, '2025-4332', '2025-01-25', '2025-10-25'),
-- (208, '2025-4334', '2025-03-01', '2026-02-28'),
-- (209, '2025-4336', '2025-01-05', '2025-10-05'),
-- (210, '2025-4338', '2025-02-10', '2025-11-10');


-- INSERT INTO Pays (PaidRoom, PayingTenant, PaymentAmount, PaymentDate) VALUES
-- -- Male tenants
-- (301, '2025-4322', 2000.00, '2025-04-01'),
-- (302, '2025-4324', 2000.00, '2025-04-02'),
-- (303, '2025-4327', 2000.00, '2025-04-03'),
-- (304, '2025-4329', 2000.00, '2025-03-30'),
-- (305, '2025-4331', 2000.00, '2025-04-01'),
-- (306, '2025-4333', 2000.00, '2025-04-04'),
-- (307, '2025-4335', 2000.00, '2025-04-05'),
-- (308, '2025-4337', 2000.00, '2025-03-31'),
-- (309, '2025-4339', 2000.00, '2025-04-02'),
-- (310, '2025-4340', 2000.00, '2025-04-06'),
-- -- Female tenants
-- (201, '2025-4321', 2000.00, '2025-04-01'),
-- (202, '2025-4323', 2000.00, '2025-04-02'),
-- (203, '2025-4325', 2000.00, '2025-04-03'),
-- (204, '2025-4326', 2000.00, '2025-03-30'),
-- (205, '2025-4328', 2000.00, '2025-04-01'),
-- (206, '2025-4330', 2000.00, '2025-04-04'),
-- (207, '2025-4332', 2000.00, '2025-04-05'),
-- (208, '2025-4334', 2000.00, '2025-03-31'),
-- (209, '2025-4336', 2000.00, '2025-04-02'),
-- (210, '2025-4338', 2000.00, '2025-04-06');

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