# CCC151-Group--BH-Management-System
## *Sistore Boarding House Management System*

### <p> Final Project for CCC151

> In partial fulfillment of the requirements in CCC151: <br>
> <div style = "text-align: center;">(Information Management)</div> 

<div>

<p> I. Abstract </p>

<p> The  Sistore Boarding House Management System is a software solution designed to streamline and offer seamless management experience for the busy Landlord of Sistore Boarding House by keeping tenant records in a presentable desktop GUI application and allowing them to seamlessly contact their tenants via Email. </p>

<p> The Sistore Boarding House Management System simplifies room assignment by allowing landlords to manage room availability, track the number of occupants per room, and adjust rental pricing accordingly. The Sistore Boarding House Management System reduces manual workload and improves management efficiency making it a valuable tool for property owners. </p>

</div>

**By:** <br>
Group 1 - CS2 <br>
[JOHN-RONAN BEIRA](https://github.com/Operator-Eury) <br>
[JOSHUA LOUISE VILLANUEVA](https://github.com/fallerfare) <br>
[KRISTELLE MARIE YBANEZ](https://github.com/Kris2103) <br>
---
![Static Badge](https://img.shields.io/badge/Database%20Schematic-MySQL%20Setup-lightblue?style=for-the-badge&logo=MySQL&logoColor=black&logoSize=auto&labelColor=dcebfa&color=a2b8ff)
```
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
    FOREIGN KEY (RentedRoom) REFERENCES Room(RoomNumber)		
		ON DELETE RESTRICT
	            ON UPDATE CASCADE,    
     FOREIGN KEY (RentingTenant) REFERENCES Tenant(TenantID) 	
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

	FOREIGN KEY (PayingTenant) REFERENCES Tenant(TenantID)		
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	FOREIGN KEY (PaidRoom) REFERENCES Room(RoomNumber)		
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

```
