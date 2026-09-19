# Storage module for VIT Student Command Center
# Handles reading and writing data to JSON files in the data directory

import json
import os
from pathlib import Path
from models import Student, Subject, Assignment, Expense, StudyTask


class JSONStorage:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        # Create data directory if it doesn't exist yet
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, filename):
        return self.data_dir / filename

    def load_json(self, filename, default_value=None):
        """Loads data from a JSON file, or returns default if file doesn't exist."""
        filepath = self._get_path(filename)
        if not filepath.exists():
            return default_value if default_value is not None else []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default_value if default_value is not None else []

    def save_json(self, filename, data):
        """Saves data to a JSON file formatted with 4-space indentation."""
        filepath = self._get_path(filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            print(f"Error saving {filename}: {e}")

    # --- Student Profile ---
    def load_student(self):
        data = self.load_json("student.json", {})
        if data:
            return Student(
                name=data.get("name", "Sarthak Dhawan"),
                registration_no=data.get("registration_no", "26BAI10618"),
                semester=data.get("semester", "1"),
                branch=data.get("branch", "Computer Science (AI and ML)")
            )
        return Student()

    def save_student(self, student):
        self.save_json("student.json", student.to_dict())

    # --- Subjects ---
    def load_subjects(self):
        data = self.load_json("subjects.json", [])
        subjects = []
        for item in data:
            subjects.append(Subject(
                name=item["name"],
                marks=float(item.get("marks", 0)),
                max_marks=float(item.get("max_marks", 100)),
                attendance=float(item.get("attendance", 75))
            ))
        return subjects

    def save_subjects(self, subjects):
        self.save_json("subjects.json", [s.to_dict() for s in subjects])

    # --- Assignments ---
    def load_assignments(self):
        data = self.load_json("assignments.json", [])
        assignments = []
        for item in data:
            assignments.append(Assignment(
                title=item["title"],
                subject=item["subject"],
                due_date=item["due_date"],
                status=item.get("status", "Pending")
            ))
        return assignments

    def save_assignments(self, assignments):
        self.save_json("assignments.json", [a.to_dict() for a in assignments])

    # --- Expenses ---
    def load_expenses(self):
        data = self.load_json("expenses.json", [])
        expenses = []
        for item in data:
            expenses.append(Expense(
                category=item["category"],
                amount=float(item["amount"]),
                note=item.get("note", ""),
                date=item.get("date", "")
            ))
        return expenses

    def save_expenses(self, expenses):
        self.save_json("expenses.json", [e.to_dict() for e in expenses])

    # --- Study Tasks ---
    def load_study_tasks(self):
        data = self.load_json("study_tasks.json", [])
        tasks = []
        for item in data:
            tasks.append(StudyTask(
                subject=item["subject"],
                topic=item["topic"],
                minutes=int(item.get("minutes", 30)),
                status=item.get("status", "Pending")
            ))
        return tasks

    def save_study_tasks(self, tasks):
        self.save_json("study_tasks.json", [t.to_dict() for t in tasks])
