from sqlalchemy import Column, Integer, String, Date
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=True)
    gender = Column(String)
    student_id = Column(String, unique=True, index=True)
    study_programme = Column(String)
    secondary_school = Column(String)
    registration_date = Column(Date)
    academic_year = Column(Integer, nullable=True) 