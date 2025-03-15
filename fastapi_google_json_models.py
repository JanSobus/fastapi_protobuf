"""Pydantic models for Google protobuf messages."""

from datetime import datetime

from pydantic import BaseModel


class Student(BaseModel):
    """Student model."""

    name: str
    avg_grade: float
    dob: datetime


class Classroom(BaseModel):
    """Classroom model."""

    profile: str
    students: list[Student]


class ClassStats(BaseModel):
    """Class statistics model."""

    numstudents: int
    grade: float
