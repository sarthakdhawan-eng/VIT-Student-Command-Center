# Data models for VIT Student Command Center
# Represents all entities: Student, Subject, Assignment, Expense, and StudyTask

from dataclasses import dataclass, asdict


@dataclass
class Student:
    name: str = "Sarthak Dhawan"
    registration_no: str = "26BAI10618"
    semester: str = "1"
    branch: str = "Computer Science (AI and ML)"

    def to_dict(self):
        return asdict(self)


@dataclass
class Subject:
    name: str
    marks: float
    max_marks: float = 100.0
    attendance: float = 75.0

    def to_dict(self):
        return asdict(self)


@dataclass
class Assignment:
    title: str
    subject: str
    due_date: str
    status: str = "Pending"

    def to_dict(self):
        return asdict(self)


@dataclass
class Expense:
    category: str
    amount: float
    note: str
    date: str

    def to_dict(self):
        return asdict(self)


@dataclass
class StudyTask:
    subject: str
    topic: str
    minutes: int
    status: str = "Pending"

    def to_dict(self):
        return asdict(self)
