from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class CourseSchema(BaseModel):
    name: str


class CourseDB(CourseSchema):
    id: int

    def as_dict(self):
        course_dict = {"id": self.id, "name": self.name}
        return course_dict


class CareerSchema(BaseModel):
    name: str
    courses: List[CourseDB]


class CareerDB(CareerSchema):
    id: int

    def as_dict(self):
        career_dict = {
            "id": self.id,
            "name": self.name,
        }

        career_dict["courses"] = [course.dict() for course in self.courses]

        return career_dict


class LeadSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    inscription_year: date
    career_id: int
    number_of_times_taken: int
    courses: List[int]


class LeadDB(LeadSchema):
    id: int
    created_date: datetime

    def as_dict(self):
        lead_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "inscription_year": self.inscription_year.isoformat(),
            "career_id": self.career_id,
            "created_date": self.created_date.isoformat(),
        }
        lead_dict["courses"] = [course for course in self.courses]
        return lead_dict


class LeadDetailedDB(BaseModel):
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    inscription_year: date
    career_id: int
    number_of_times_taken: int
    courses: List[int]

    def as_dict(self):
        lead_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "inscription_year": self.inscription_year.isoformat(),
            "career_id": self.career_id,
        }
        lead_dict["courses"] = [course.id for course in self.courses]
        return lead_dict
