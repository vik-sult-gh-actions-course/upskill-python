from db import Base
from sqlalchemy import Column, Integer, String, Boolean, Text


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    code = Column(String(200))
    email = Column(String(50))
    head = Column(String(200))
    budget = Column(String(20))
    location = Column(String(50))
    phone = Column(String(20))
    manager = Column(String(50))
    size = Column(Integer)
    creation_date = Column(String(10))


class People(Base):
    __tablename__ = 'people'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    gender = Column(String(50))
    phone_number = Column(String(50))
    job_title = Column(String(50))
    department = Column(String(20))
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    start_time = Column(String(20))
    end_time = Column(String(20))
    salary = Column(String(20))
    hire_date = Column(String(20))
    manager_id = Column(Integer)
    age = Column(Integer)
    years_of_experience = Column(Integer)
