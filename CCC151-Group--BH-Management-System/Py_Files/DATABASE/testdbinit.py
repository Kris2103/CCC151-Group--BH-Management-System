from sqlalchemy import create_engine, Column, ForeignKeyConstraint, VARCHAR, DECIMAL, Integer, MetaData, text, DATE, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import pandas as pd
from db_config import DB_USER, DB_PASSWORD, DB_HOST

#==================
#  SETUP DATABASE
#==================

# Initialize Connection
Base = declarative_base()
connection_str  = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/sistonemanagement'

try: 
    engine          = create_engine(connection_str, echo = True)
    connection      = engine.connect()

# Create database if it doesn't exist yet 
except OperationalError as e:
    if "1049" in str(e.orig):
        engine      = create_engine(connection_str - "sistonemanagement", echo=True)
        connection  = engine.connect()
        connection.execute(text("CREATE DATABASE sistonemanagement"))
        connection.close()

        # Now reconnect
        engine = create_engine(connection_str, echo=True)
        connection = engine.connect()

# Super Table
class BaseTable(Base):
    __abstract__ = True

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def update(self, session, table, id, values):
        session.update(table).where(table.c["ID Number"] == id).values(**values)
        session.commit()
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return str(self.to_dict())

# Tenants Model
class Tenants(BaseTable):
    __tablename__ = "tenants"

    t_id = Column("Tenant ID",          VARCHAR(9),     nullable = False,   primary_key = True, unique = True)
    t_fn = Column("First Name",         VARCHAR(128),   nullable = False)
    t_mn = Column("Middle Name",        VARCHAR(128),   nullable = True)
    t_ln = Column("Last Name",          VARCHAR(128),   nullable = False)
    t_em = Column("Email",              VARCHAR(255),   nullable = False)
    t_sx = Column("Sex",                VARCHAR(6),     nullable = False)
    t_pn = Column("Phone Number",       VARCHAR(100),   nullable = False)
    t_rm = Column("Room Number",        Integer,        nullable = False,   foreign_key = True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["Room Number"], ["rooms.Room Number"],
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        UniqueConstraint('First Name', 'Middle Name', 'Last Name', name = 'tenant_fullname'),
        UniqueConstraint('Email', 'Phone Number', name = 'tenant_contact'),
    )

    def __init__(self, t_id, t_fn, t_mn, t_ln, t_em, t_sx, t_pn, t_rm):

        self.t_id = t_id
        self.t_fn = t_fn 
        self.t_mn = t_mn
        self.t_ln = t_ln
        self.t_em = t_em 
        self.t_sx = t_sx
        self.t_pn = t_pn
        self.t_rm = t_rm

# Rooms Model
class Rooms(BaseTable):
    __tablename__ = "rooms"

    r_id = Column("Room Number",          Integer,       nullable = False,   primary_key = True, unique = True)
    r_pr = Column("Price",                DECIMAL(5, 2),     nullable = False)
    r_tx = Column("Tenant Sex",           VARCHAR(6),       nullable = False)
    r_mx = Column("Maximum Capacity",     Integer,          nullable = False)
    r_no = Column("No. of Occupants",     Integer,          nullable = False)

    def __init__(self, r_id, r_pr, r_tx, r_mx, r_no):

        self.r_id = r_id
        self.r_pr = r_pr
        self.r_tx = r_tx
        self.r_mx = r_mx
        self.r_no = r_no

# Emergency Contact Model
class EmergencyContact(BaseTable):
    __tablename__ = "emergencycontact"

    e_id = Column("Emergency Contact ID",   VARCHAR(9),     nullable = False,   primary_key = True, unique = True)
    e_fn = Column("First Name",             VARCHAR(128),   nullable = False)
    e_mn = Column("Middle Name",            VARCHAR(128),   nullable = True)
    e_ln = Column("Last Name",              VARCHAR(128),   nullable = False)
    e_pn = Column("Phone Number",           VARCHAR(100),   nullable = False)
    e_re = Column("Relationship",           VARCHAR(128),   nullable = False)
    e_tn = Column("Tenant ID",              VARCHAR(9),     nullable = False,   foreign_key = True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["Tenant ID"], ["tenants.Tenant ID"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
    )

    def __init__(self, e_id, e_fn, e_mn, e_ln, e_pn, e_re, e_tn):

        self.e_id = e_id
        self.e_fn = e_fn 
        self.e_mn = e_mn
        self.e_ln = e_ln
        self.e_pn = e_pn 
        self.e_re = e_re
        self.e_tn = e_tn

# Payments Model
class Payments(BaseTable):
    __tablename__ = "payments"

    p_id = Column("Payment ID",             Integer,        nullable = False,   primary_key = True, unique = True, autoincrement = True)
    p_am = Column("Payment Amount",         DECIMAL(5, 2),   nullable = False)
    p_dt = Column("Payment Date",           DATE,           nullable = False)
    p_pn = Column("Payment Status",         VARCHAR(10),    nullable = False)
    p_tn = Column("Paying Tenant",          VARCHAR(9),     nullable = False,   foreign_key = True)
    p_rm = Column("Paid Room",              Integer,        nullable = False,   foreign_key = True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["Paying Tenant"], ["tenants.Tenant ID"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        ForeignKeyConstraint(
            ["Paid Room"], ["rooms.Room Number"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
    )

    def __init__(self, p_id, p_am, p_dt, p_pn, p_tn, p_rm):

        self.p_id = p_id
        self.p_am = p_am 
        self.p_dt = p_dt
        self.p_pn = p_pn
        self.p_tn = p_tn 
        self.p_rm = p_rm

# Payments Model
class Rentals(BaseTable):
    __tablename__ = "rentals"

    n_id = Column("Rental ID",              Integer,        nullable = False,   primary_key = True, unique = True, autoincrement = True)
    n_mi = Column("Move In Date",           DATE,           nullable = False)
    n_mo = Column("Move Out Date",          DATE,           nullable = True)
    n_ms = Column("Move Status",            VARCHAR(50),    nullable = False)
    n_tn = Column("Renting Tenant",         VARCHAR(9),     nullable = False,   foreign_key = True)
    n_rm = Column("Rented Room",            Integer,        nullable = False,   foreign_key = True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["Renting Tenant"], ["tenants.Tenant ID"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
        ForeignKeyConstraint(
            ["Rented Room"], ["rooms.Room Number"],
            ondelete="CASCADE",
            onupdate="CASCADE"
        ),
    )

    def __init__(self, n_id, n_mi, n_mo, n_ms, n_tn, n_rm):

        self.n_id = n_id
        self.n_mi = n_mi 
        self.n_mo = n_mo
        self.n_ms = n_ms
        self.n_tn = n_tn 
        self.n_rm = n_rm

# Load existing data on database
Base.metadata.create_all(bind = engine)
metadata = MetaData()
metadata.reflect(bind=engine)

# Create session for queries
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

#==================
#  SETUP DATABASE
#==================


#==================
# RETURN DATAFRAMES
#==================

def tenantsModel():
    return pd.read_sql_table("tenants", con = engine)

def roomsModel():
    return pd.read_sql_table("rooms", con = engine)

def paymentssModel():
    return pd.read_sql_table("payments", con = engine)

def rentalsModel():
    return pd.read_sql_table("rentals", con = engine)

#==================
# RETURN DATAFRAMES
#==================