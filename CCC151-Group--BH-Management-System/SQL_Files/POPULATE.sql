-- Populate Room
INSERT INTO Room (RoomNumber, Price, TenantSex, MaximumCapacity) VALUES
(101, 5000.00, 'Male', 2),
(102, 5200.00, 'Female', 2),
(103, 4800.00, 'Male', 1),
(104, 5300.00, 'Female', 3),
(105, 5000.00, NULL, 4),
(106, 5100.00, 'Male', 2),
(107, 4950.00, 'Female', 1),
(108, 5500.00, NULL, 3),
(109, 4700.00, 'Male', 2),
(110, 6000.00, 'Female', 2);

-- Populate Tenant
INSERT INTO Tenant (TenantID, Email, FirstName, MiddleName, LastName, Sex, PhoneNumber, RoomNumber) VALUES
('2023-0001', 'alice@gmail.com', 'Alice', 'Marie', 'Santos', 'Female', '09171234567', 102),
('2023-0002', 'bob@gmail.com', 'Bob', NULL, 'Reyes', 'Male', '09181234568', 101),
('2023-0003', 'carla@gmail.com', 'Carla', 'M.', 'Lopez', 'Female', '09192234569', 102),
('2023-0004', 'daniel@gmail.com', 'Daniel', NULL, 'Cruz', 'Male', '09173334567', 101),
('2023-0005', 'ellen@gmail.com', 'Ellen', 'Joy', 'Flores', 'Female', '09184444567', NULL),
('2023-0006', 'frank@gmail.com', 'Frank', NULL, 'Torres', 'Male', '09195555567', NULL),
('2023-0007', 'gina@gmail.com', 'Gina', 'S.', 'Navarro', 'Female', '09176666667', NULL),
('2023-0008', 'henry@gmail.com', 'Henry', NULL, 'Dela Cruz', 'Male', '09187777767', 106),
('2023-0009', 'irene@gmail.com', 'Irene', 'L.', 'Bautista', 'Female', '09198888867', 107),
('2023-0010', 'jack@gmail.com', 'Jack', NULL, 'Villanueva', 'Male', '09209999967', 106),
('2023-0011', 'kate@gmail.com', 'Kate', 'Ann', 'Padilla', 'Female', '09170000011', 104),
('2023-0012', 'leo@gmail.com', 'Leo', NULL, 'Garcia', 'Male', '09171111112', 103),
('2023-0013', 'maya@gmail.com', 'Maya', 'K.', 'Rivera', 'Female', '09172222213', 104),
('2023-0014', 'nash@gmail.com', 'Nash', NULL, 'Alvarez', 'Male', '09173333314', 109),
('2023-0015', 'olga@gmail.com', 'Olga', 'M.', 'Gomez', 'Female', '09174444415', NULL),
('2023-0016', 'paul@gmail.com', 'Paul', NULL, 'Mendoza', 'Male', '09175555516', 109),
('2023-0017', 'quinn@gmail.com', 'Quinn', 'S.', 'De Leon', 'Female', '09176666617', 104),
('2023-0018', 'ray@gmail.com', 'Ray', NULL, 'Domingo', 'Male', '09177777718', 101),
('2023-0019', 'sara@gmail.com', 'Sara', 'L.', 'Vergara', 'Female', '09178888819', 108),
('2023-0020', 'tom@gmail.com', 'Tom', NULL, 'Diaz', 'Male', '09179999920', 110);

-- Populate Rents
INSERT INTO Rents (RentingTenant, RentedRoom, MoveInDate, MoveOutDate) VALUES
('2023-0001', 102, '2025-01-01', '2025-06-30'),
('2023-0002', 101, '2025-01-15', '2025-07-15'),
('2023-0003', 102, '2025-02-01', '2025-08-01'),
('2023-0004', 101, '2025-01-20', '2025-06-20'),
('2023-0005', 104, '2025-03-01', '2025-09-01'),
('2023-0006', 103, '2025-04-01', '2025-10-01'),
('2023-0007', 104, '2025-02-15', '2025-08-15'),
('2023-0008', 106, '2025-01-10', '2025-07-10'),
('2023-0009', 107, '2025-02-20', '2025-08-20'),
('2023-0010', 106, '2025-03-01', '2025-09-01'),
('2023-0011', 104, '2025-01-01', '2025-06-30'),
('2023-0012', 103, '2025-01-10', '2025-07-10'),
('2023-0013', 104, '2025-04-01', '2025-10-01'),
('2023-0014', 109, '2025-05-01', '2025-11-01'),
('2023-0015', 107, '2025-06-01', '2025-12-01'),
('2023-0016', 109, '2025-01-15', '2025-07-15'),
('2023-0017', 104, '2025-02-01', '2025-08-01'),
('2023-0018', 101, '2025-03-01', '2025-09-01'),
('2023-0019', 108, '2025-04-01', '2025-10-01'),
('2023-0020', 110, '2025-05-01', '2025-11-01');

-- Populate Pays
INSERT INTO Pays (PayingTenant, PaidRoom, PaymentAmount, PaymentDate) VALUES
('2023-0001', 102, 5000.00, '2025-01-01'),
('2023-0002', 101, 5000.00, '2025-01-15'),
('2023-0003', 102, 5000.00, '2025-02-01'),
('2023-0004', 101, 5000.00, '2025-01-20'),
('2023-0005', 104, 5300.00, '2025-03-01'),
('2023-0006', 103, 4800.00, '2025-04-01'),
('2023-0007', 104, 5300.00, '2025-02-15'),
('2023-0008', 106, 5100.00, '2025-01-10'),
('2023-0009', 107, 4950.00, '2025-02-20'),
('2023-0010', 106, 5100.00, '2025-03-01'),
('2023-0011', 104, 5300.00, '2025-01-01'),
('2023-0012', 103, 4800.00, '2025-01-10'),
('2023-0013', 104, 5300.00, '2025-04-01'),
('2023-0014', 109, 4700.00, '2025-05-01'),
('2023-0015', 107, 4950.00, '2025-06-01'),
('2023-0016', 109, 4700.00, '2025-01-15'),
('2023-0017', 104, 5300.00, '2025-02-01'),
('2023-0018', 101, 5000.00, '2025-03-01'),
('2023-0019', 108, 5500.00, '2025-04-01'),
('2023-0020', 110, 6000.00, '2025-05-01');

-- Populate EmergencyContact
INSERT INTO EmergencyContact (ContactID, FirstName, MiddleName, LastName, Relationship, PhoneNumber, EMTenantID) VALUES
('2023-1001', 'Anna', 'M.', 'Santos', 'Mother', '09180000001', '2023-0001'),
('2023-1002', 'Robert', NULL, 'Reyes', 'Father', '09180000002', '2023-0002'),
('2023-1003', 'Cynthia', 'L.', 'Lopez', 'Sister', '09180000003', '2023-0003'),
('2023-1004', 'David', NULL, 'Cruz', 'Brother', '09180000004', '2023-0004'),
('2023-1005', 'Ella', 'Joy', 'Flores', 'Aunt', '09180000005', '2023-0005'),
('2023-1006', 'Felix', NULL, 'Torres', 'Uncle', '09180000006', '2023-0006'),
('2023-1007', 'Grace', 'S.', 'Navarro', 'Mother', '09180000007', '2023-0007'),
('2023-1008', 'Helen', NULL, 'Dela Cruz', 'Sister', '09180000008', '2023-0008'),
('2023-1009', 'Ivan', 'L.', 'Bautista', 'Brother', '09180000009', '2023-0009'),
('2023-1010', 'Jessica', NULL, 'Villanueva', 'Mother', '09180000010', '2023-0010'),
('2023-1011', 'Kevin', 'A.', 'Padilla', 'Father', '09180000011', '2023-0011'),
('2023-1012', 'Lara', NULL, 'Garcia', 'Sister', '09180000012', '2023-0012'),
('2023-1013', 'Monica', 'K.', 'Rivera', 'Mother', '09180000013', '2023-0013'),
('2023-1014', 'Nathan', NULL, 'Alvarez', 'Father', '09180000014', '2023-0014'),
('2023-1015', 'Olive', 'M.', 'Gomez', 'Aunt', '09180000015', '2023-0015'),
('2023-1016', 'Peter', NULL, 'Mendoza', 'Uncle', '09180000016', '2023-0016'),
('2023-1017', 'Queen', 'S.', 'De Leon', 'Sister', '09180000017', '2023-0017'),
('2023-1018', 'Rachel', NULL, 'Domingo', 'Mother', '09180000018', '2023-0018'),
('2023-1019', 'Steven', 'L.', 'Vergara', 'Brother', '09180000019', '2023-0019'),
('2023-1020', 'Tina', NULL, 'Diaz', 'Mother', '09180000020', '2023-0020');


-- Additional filler data with null

INSERT INTO Tenant (TenantID, Email, FirstName, MiddleName, LastName, Sex, PhoneNumber, RoomNumber) VALUES
('2023-0021', 'ursula@gmail.com', 'Ursula', 'Mae', 'Jimenez', 'Female', '09201111121', NULL),
('2023-0022', 'victor@gmail.com', 'Victor', NULL, 'Tan', 'Male', '09202222222', NULL),
('2023-0023', 'wendy@gmail.com', 'Wendy', 'T.', 'Cabrera', 'Female', '09203333323', NULL),
('2023-0024', 'xander@gmail.com', 'Xander', NULL, 'Lim', 'Male', '09204444424', NULL),
('2023-0025', 'yara@gmail.com', 'Yara', 'N.', 'Castro', 'Female', '09205555525', NULL),
('2023-0026', 'zack@gmail.com', 'Zack', NULL, 'Silva', 'Male', '09206666626', NULL),
('2023-0027', 'abby@gmail.com', 'Abby', 'R.', 'Ortega', 'Female', '09207777727', NULL),
('2023-0028', 'ben@gmail.com', 'Ben', NULL, 'Fernandez', 'Male', '09208888828', NULL),
('2023-0029', 'cathy@gmail.com', 'Cathy', 'J.', 'Chua', 'Female', '09209999929', NULL),
('2023-0030', 'dave@gmail.com', 'Dave', NULL, 'Aquino', 'Male', '09300000030', NULL),
('2023-0031', 'ellaine@gmail.com', 'Ellaine', 'P.', 'Reyes', 'Female', '09301111131', NULL),
('2023-0032', 'fred@gmail.com', 'Fred', NULL, 'Salvador', 'Male', '09302222232', NULL),
('2023-0033', 'giselle@gmail.com', 'Giselle', 'F.', 'Romero', 'Female', '09303333333', NULL),
('2023-0034', 'hugo@gmail.com', 'Hugo', NULL, 'Gatchalian', 'Male', '09304444434', NULL),
('2023-0035', 'ivy@gmail.com', 'Ivy', 'K.', 'Sy', 'Female', '09305555535', NULL),
('2023-0036', 'jose@gmail.com', 'Jose', NULL, 'Tan', 'Male', '09306666636', NULL),
('2023-0037', 'karla@gmail.com', 'Karla', 'L.', 'Bermudez', 'Female', '09307777737', NULL),
('2023-0038', 'luke@gmail.com', 'Luke', NULL, 'Agustin', 'Male', '09308888838', NULL),
('2023-0039', 'mia@gmail.com', 'Mia', 'V.', 'Lagman', 'Female', '09309999939', NULL),
('2023-0040', 'nate@gmail.com', 'Nate', NULL, 'Quinto', 'Male', '09400000040', NULL);

INSERT INTO Room (RoomNumber, Price, TenantSex, MaximumCapacity) VALUES
(201, 5050.00, NULL, 2),
(202, 5150.00, NULL, 1),
(203, 5250.00, NULL, 3),
(204, 5350.00, NULL, 2),
(205, 5450.00, NULL, 4),
(206, 5550.00, NULL, 1),
(207, 5650.00, NULL, 2),
(208, 5750.00, NULL, 3),
(209, 5850.00, NULL, 2),
(210, 5950.00, NULL, 1);
 
 INSERT INTO EmergencyContact (ContactID, FirstName, MiddleName, LastName, Relationship, PhoneNumber, EMTenantID) VALUES
('2023-1021', 'Uma', 'P.', 'Jimenez', 'Mother', '09410000021', '2023-0021'),
('2023-1022', 'Vera', NULL, 'Tan', 'Sister', '09410000022', '2023-0022'),
('2023-1023', 'Wally', 'G.', 'Cabrera', 'Father', '09410000023', '2023-0023'),
('2023-1024', 'Xena', NULL, 'Lim', 'Mother', '09410000024', '2023-0024'),
('2023-1025', 'Yosef', 'T.', 'Castro', 'Brother', '09410000025', '2023-0025'),
('2023-1026', 'Zara', NULL, 'Silva', 'Aunt', '09410000026', '2023-0026'),
('2023-1027', 'Andrew', 'R.', 'Ortega', 'Uncle', '09410000027', '2023-0027'),
('2023-1028', 'Bea', NULL, 'Fernandez', 'Mother', '09410000028', '2023-0028'),
('2023-1029', 'Carlos', 'J.', 'Chua', 'Father', '09410000029', '2023-0029'),
('2023-1030', 'Diane', NULL, 'Aquino', 'Sister', '09410000030', '2023-0030'),
('2023-1031', 'Edwin', 'P.', 'Reyes', 'Uncle', '09410000031', '2023-0031'),
('2023-1032', 'Faith', NULL, 'Salvador', 'Aunt', '09410000032', '2023-0032'),
('2023-1033', 'Greg', 'F.', 'Romero', 'Father', '09410000033', '2023-0033'),
('2023-1034', 'Hannah', NULL, 'Gatchalian', 'Mother', '09410000034', '2023-0034'),
('2023-1035', 'Ian', 'K.', 'Sy', 'Brother', '09410000035', '2023-0035');
