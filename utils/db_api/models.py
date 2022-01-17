from sqlalchemy import (Column, Integer, String, DateTime, BigInteger, ForeignKey, Boolean, Float, Text, Constraint)

from utils.db_api.database import db


class Student(db.Model):
    __tablename__ = "students_udemy"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    telegram_id = Column(BigInteger, nullable=True)
    github_username = Column(String(length=100), nullable=True)

    student_name = Column(String(length=100))
    udemy_for_business = Column(String(length=100))
    enrolled = Column(DateTime, unique=True)
    started_date = Column(DateTime, nullable=True)
    last_visited = Column(DateTime, nullable=True)
    lecture_last_viewed = Column(String(length=200))
    progress = Column(Integer)
    questions_asked = Column(Integer)
    questions_answered = Column(Integer)
