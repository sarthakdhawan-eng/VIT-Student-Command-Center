# VIT Student Command Center
# Student Name: Sarthak Dhawan
# Registration No: 26BAI10618
# Course: Python Programming (Python Essentials Project)
# Description: All-in-one console application for managing student
# academics, attendance, assignments, expenses, and tasks.

from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, cast

from models import Assignment, Expense, StudyTask, Subject
from storage import JSONStorage
from ui import (
    banner as _ui_banner, # type: ignore
    clear_screen,
    color, # type: ignore
    error, #type: ignore
    loading, #type: ignore
    pause,
    progress_bar, #type: ignore
    section, #type: ignore
    success, #type: ignore
    table, #type: ignore
    warning, #type: ignore
    Colors,
)

# Give the imported UI helper an explicit signature for static type checkers.
banner = cast(Callable[[str, str], None], _ui_banner)

class StudentCommandCenter:
    def __init__(self):
        # Set up storage in the data/ folder next to this file
        base_folder = Path(__file__).parent / "data"
        self.storage = JSONStorage(str(base_folder))

        # Load all user data from JSON files
        self.student: Any = self.storage.load_student()
        self.subjects: list[Subject] = self.storage.load_subjects()
        self.assignments: list[Assignment] = self.storage.load_assignments()
        self.expenses: list[Expense] = self.storage.load_expenses()
        self.study_tasks: list[StudyTask] = self.storage.load_study_tasks()

        # Pre-populate sample subjects if first time running
        self._seed_demo_data()

    def _seed_demo_data(self):
        #Adds starter subjects for first-time setup if none exist.
        if not self.subjects:
            self.subjects = [
                Subject("Python", 84, 100, 91),
                Subject("Mathematics", 76, 100, 86),
                Subject("Physics", 72, 100, 79),
                Subject("English", 88, 100, 95),
            ]
            self.storage.save_subjects(self.subjects) #type: ignore
            loading("Initializing student workspace")

    def run(self):
        #Main application execution loop.
        while True:
            clear_screen()
            self.dashboard()
            choice = input("\n  Enter choice ➜ ").strip()

            if choice == "1":
                self.academic_menu()
            elif choice == "2":
                self.assignment_menu()
            elif choice == "3":
                self.expense_menu()
            elif choice == "4":
                self.attendance_menu()
            elif choice == "5":
                self.study_menu()
            elif choice == "6":
                self.profile_menu()
            elif choice == "7":
                self.save_all()
            elif choice == "8":
                self.exit_app()
                break
            else:
                error("Invalid choice. Please choose a number between 1 and 8.")
                pause()

    def dashboard(self):
        #Renders the top summary banner and main navigation menu.
        banner("VIT STUDENT COMMAND CENTER", "Python Essentials Project")

        # Student Details
        print(f"\n  Student : {color(self.student.name, Colors.BOLD)}")
        print(f"  Reg. No : {self.student.registration_no}")
        print(f"  Branch  : {self.student.branch}") # type: ignore
        print(f"  Semester: {self.student.semester}")

        # Quick calculations for dashboard summary
        avg = self._average_marks()
        attendance = self._average_attendance()
        pending_assignments = sum(1 for a in self.assignments if a.status.lower() != "completed")
        expense_total = sum(e.amount for e in self.expenses)

        section("Live Dashboard")
        print(f"  Academic Average  : {avg:.1f}%   {progress_bar(avg)}")
        print(f"  Overall Attendance: {attendance:.1f}%   {progress_bar(attendance)}")
        print(f"  Pending Work      : {pending_assignments} assignment(s)")
        print(f"  Expenses Recorded : ₹{expense_total:,.2f}")

        section("Main Menu")
        menu_items = [
            ("1", "Academic Performance"),
            ("2", "Assignment Manager"),
            ("3", "Expense Tracker"),
            ("4", "Attendance Calculator"),
            ("5", "Study Planner"),
            ("6", "Student Profile"),
            ("7", "Save All Data"),
            ("8", "Exit"),
        ]
        for num, label in menu_items:
            print(f"  [{num}] {label}")

    # 1. ACADEMIC PERFORMANCE
    def academic_menu(self):
        clear_screen()
        banner("ACADEMIC PERFORMANCE") #type: ignore
        section("Subject Scorecard")

        rows = []
        for s in self.subjects:
            pct = (s.marks / s.max_marks * 100) if s.max_marks > 0 else 0
            grade = self._calculate_grade(pct) #type: ignore
            rows.append([s.name, f"{s.marks:g}/{s.max_marks:g}", f"{pct:.1f}%", grade]) #type: ignore

        table(["Subject", "Marks", "Percentage", "Grade"], rows)
        print(f"\n  Overall Average: {self._average_marks():.2f}%")

        choice = input("\n  Press [A] to add/update a subject, [B] to go back ➜ ").strip().lower()
        if choice == "a":
            name = input("  Subject name: ").strip().title()
            if not name:
                error("Subject name cannot be empty.")
                pause()
                return

            marks = self._read_float("  Marks obtained: ", minimum=0) #type: ignore
            max_marks = self._read_float("  Maximum marks: ", minimum=1) #type: ignore
            attendance = self._read_float("  Attendance %: ", minimum=0, maximum=100) #type: ignore

            # Check if subject already exists to update it
            existing_sub = None
            for sub in self.subjects:
                if sub.name.lower() == name.lower():
                    existing_sub = sub
                    break

            if existing_sub:
                existing_sub.marks = marks
                existing_sub.max_marks = max_marks
                existing_sub.attendance = attendance
                success(f"Updated record for '{existing_sub.name}'.")
            else:
                self.subjects.append(Subject(name, marks, max_marks, attendance))
                success(f"Added subject '{name}'.")

            self.storage.save_subjects(self.subjects) #type: ignore
            pause()

    def _average_marks(self):
        if not self.subjects:
            return 0.0
        total_pct = sum((s.marks / s.max_marks * 100) for s in self.subjects if s.max_marks > 0)
        return total_pct / len(self.subjects)

    def _average_attendance(self):
        if not self.subjects:
            return 0.0
        return sum(s.attendance for s in self.subjects) / len(self.subjects)

    @staticmethod
    def _calculate_grade(percentage): #type: ignore
        #Determines letter grade using standard grading scale.
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B+"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        else:
            return "F"

    # 2. ASSIGNMENT MANAGER
    def assignment_menu(self):
        while True:
            clear_screen()
            banner("ASSIGNMENT MANAGER") #type:ignore

            rows = []
            for idx, a in enumerate(self.assignments, start=1):
                rows.append([str(idx), a.title, a.subject, a.due_date, a.status]) #type: ignore

            table(["#", "Title", "Subject", "Due Date", "Status"], rows)

            print("\n  [1] Add assignment  [2] Complete assignment  [3] Delete assignment  [B] Back")
            choice = input("\n  Choice ➜ ").strip().lower()

            if choice == "1":
                title = input("  Assignment title: ").strip()
                subject = input("  Subject: ").strip().title()
                due_date = self._read_date("  Due date (YYYY-MM-DD): ")

                self.assignments.append(Assignment(title, subject, due_date))
                self.storage.save_assignments(self.assignments)
                success("Assignment added successfully.")
                pause()

            elif choice == "2":
                idx = self._read_index(len(self.assignments), "  Assignment number to mark complete: ")
                if idx is not None:
                    self.assignments[idx].status = "Completed"
                    self.storage.save_assignments(self.assignments)
                    success("Assignment marked as completed!")
                    pause()

            elif choice == "3":
                idx = self._read_index(len(self.assignments), "  Assignment number to delete: ")
                if idx is not None:
                    removed = self.assignments.pop(idx)
                    self.storage.save_assignments(self.assignments)
                    success(f"Deleted assignment '{removed.title}'.")
                    pause()

            elif choice == "b":
                break
            else:
                error("Invalid option. Please try again.")
                pause()

    # =================================================================
    # 3. EXPENSE TRACKER
    # =================================================================
    def expense_menu(self):
        while True:
            clear_screen()
            banner("EXPENSE TRACKER")

            total_spent = sum(e.amount for e in self.expenses)
            print(f"\n  Total Spending: {color(f'₹{total_spent:,.2f}', Colors.BOLD)}")

            # Calculate category breakdown
            category_totals = {}
            for e in self.expenses:
                category_totals[e.category] = category_totals.get(e.category, 0.0) + e.amount

            if category_totals:
                section("Category Breakdown")
                breakdown_rows = []
                for cat, amt in sorted(category_totals.items()):
                    share = (amt / total_spent * 100) if total_spent > 0 else 0
                    breakdown_rows.append([cat, f"₹{amt:,.2f}", f"{share:.1f}%"])
                table(["Category", "Amount", "Share"], breakdown_rows)

            section("Recent Expenses")
            recent = self.expenses[-10:]  # Show last 10 expenses
            recent_rows = []
            for idx, e in enumerate(recent, start=1):
                recent_rows.append([str(idx), e.date, e.category, f"₹{e.amount:,.2f}", e.note])
            table(["#", "Date", "Category", "Amount", "Note"], recent_rows)

            print("\n  [1] Add expense  [2] Remove expense  [B] Back")
            choice = input("\n  Choice ➜ ").strip().lower()

            if choice == "1":
                category = input("  Category (e.g. Food, Books, Travel): ").strip().title()
                amount = self._read_float("  Amount: ₹", minimum=0.01)
                note = input("  Short note: ").strip()
                today_str = date.today().isoformat()

                self.expenses.append(Expense(category, amount, note, today_str))
                self.storage.save_expenses(self.expenses)
                success("Expense recorded.")
                pause()

            elif choice == "2":
                idx = self._read_index(len(self.expenses), "  Expense number to remove (from recent list): ")
                if idx is not None:
                    # Map recent display index to actual list index
                    actual_idx = len(self.expenses) - len(recent) + idx
                    removed = self.expenses.pop(actual_idx)
                    self.storage.save_expenses(self.expenses)
                    success(f"Removed expense of ₹{removed.amount:.2f} ({removed.category}).")
                    pause()

            elif choice == "b":
                break
            else:
                error("Invalid option. Please try again.")
                pause()

    # =================================================================
    # 4. ATTENDANCE CALCULATOR & BUNK PLANNER
    # =================================================================
    def attendance_menu(self):
        clear_screen()
        banner("ATTENDANCE CALCULATOR")

        current_overall = self._average_attendance()
        print(f"\n  Current Average Attendance: {color(f'{current_overall:.2f}%', Colors.BOLD)}")

        section("Attendance Projection")
        conducted = self._read_int("  Total classes conducted so far: ", minimum=0)
        attended = self._read_int("  Classes attended: ", minimum=0, maximum=conducted)
        target = self._read_float("  Target attendance % (e.g. 75, 80): ", minimum=1, maximum=100)

        current_pct = (attended / conducted * 100) if conducted > 0 else 100.0
        print(f"\n  Current Attendance Rate: {current_pct:.2f}%")

        if current_pct >= target:
            # How many classes can be safely skipped?
            bunks = self._calculate_safe_bunks(attended, conducted, target)
            success(f"You are on track! You can safely miss up to {bunks} class(es) without dropping below {target:.0f}%.")
        else:
            # How many consecutive classes must be attended?
            needed = self._calculate_classes_needed(attended, conducted, target)
            warning(f"Below target! You need to attend the next {needed} consecutive class(es) to reach {target:.0f}%.")

        pause()

    @staticmethod
    def _calculate_classes_needed(attended, conducted, target):
        """Simulates how many consecutive classes are required to reach target %."""
        if conducted == 0:
            return 0

        needed = 0
        curr_att = attended
        curr_cond = conducted

        while (curr_att / curr_cond * 100) < target:
            curr_att += 1
            curr_cond += 1
            needed += 1
            if needed > 1000:  # safety limit
                break

        return needed

    @staticmethod
    def _calculate_safe_bunks(attended, conducted, target):
        """Simulates how many upcoming classes can be missed while staying >= target %."""
        if conducted == 0:
            return 0

        bunks = 0
        curr_att = attended
        curr_cond = conducted

        # Continue adding conducted classes without increasing attended
        while True:
            next_cond = curr_cond + 1
            if (curr_att / next_cond * 100) >= target:
                curr_cond = next_cond
                bunks += 1
                if bunks > 1000:  # safety limit
                    break
            else:
                break

        return bunks

    # =================================================================
    # 5. STUDY PLANNER
    # =================================================================
    def study_menu(self):
        while True:
            clear_screen()
            banner("STUDY PLANNER")

            rows = []
            for idx, task in enumerate(self.study_tasks, start=1):
                rows.append([str(idx), task.subject, task.topic, f"{task.minutes} mins", task.status])

            table(["#", "Subject", "Topic", "Duration", "Status"], rows)

            print("\n  [1] Add study task  [2] Complete task  [B] Back")
            choice = input("\n  Choice ➜ ").strip().lower()

            if choice == "1":
                subject = input("  Subject: ").strip().title()
                topic = input("  Topic: ").strip()
                minutes = self._read_int("  Planned duration in minutes: ", minimum=1)

                self.study_tasks.append(StudyTask(subject, topic, minutes))
                self.storage.save_study_tasks(self.study_tasks)
                success("Study task scheduled.")
                pause()

            elif choice == "2":
                idx = self._read_index(len(self.study_tasks), "  Task number to mark completed: ")
                if idx is not None:
                    self.study_tasks[idx].status = "Completed"
                    self.storage.save_study_tasks(self.study_tasks)
                    success("Good job! Task marked as completed.")
                    pause()

            elif choice == "b":
                break
            else:
                error("Invalid choice. Try again.")
                pause()

    # =================================================================
    # 6. STUDENT PROFILE
    # =================================================================
    def profile_menu(self):
        clear_screen()
        banner("STUDENT PROFILE")
        section("Current Details")

        print(f"  Name          : {self.student.name}")
        print(f"  Registration  : {self.student.registration_no}")
        print(f"  Branch        : {self.student.branch}")
        print(f"  Semester      : {self.student.semester}")

        print("\n  [1] Edit Profile  [B] Back")
        choice = input("\n  Choice ➜ ").strip().lower()

        if choice == "1":
            print("\n  (Leave blank to keep existing value)")
            new_name = input(f"  Name [{self.student.name}]: ").strip()
            new_reg = input(f"  Reg. No [{self.student.registration_no}]: ").strip()
            new_branch = input(f"  Branch [{self.student.branch}]: ").strip()
            new_sem = input(f"  Semester [{self.student.semester}]: ").strip()

            if new_name:
                self.student.name = new_name
            if new_reg:
                self.student.registration_no = new_reg
            if new_branch:
                self.student.branch = new_branch
            if new_sem:
                self.student.semester = new_sem

            self.storage.save_student(self.student)
            success("Profile updated successfully.")
            pause()

    # =================================================================
    # SAVE & EXIT UTILITIES
    # =================================================================
    def save_all(self):
        """Explicitly saves all in-memory lists to their respective JSON files."""
        self.storage.save_student(self.student)
        self.storage.save_subjects(self.subjects)
        self.storage.save_assignments(self.assignments)
        self.storage.save_expenses(self.expenses)
        self.storage.save_study_tasks(self.study_tasks)
        success("All data files saved successfully.")
        pause()

    def exit_app(self):
        #Saves current state and displays exit farewell.
        self.storage.save_student(self.student)
        self.storage.save_subjects(self.subjects) # type: ignore
        self.storage.save_assignments(self.assignments)
        self.storage.save_expenses(self.expenses)
        self.storage.save_study_tasks(self.study_tasks)

        clear_screen()
        banner("SEE YOU SOON!", "VIT Student Command Center")
        print(f"\n  Goodbye {self.student.name}! All your data is saved.\n")

    # =================================================================
    # USER INPUT VALIDATION HELPERS
    # =================================================================
    @staticmethod
    def _read_float(prompt, minimum=None, maximum=None):
        while True:
            raw = input(prompt).strip()
            try:
                val = float(raw)
                if minimum is not None and val < minimum:
                    error(f"Value must be at least {minimum}.")
                    continue
                if maximum is not None and val > maximum:
                    error(f"Value cannot exceed {maximum}.")
                    continue
                return val
            except ValueError:
                error("Please enter a valid numeric value.")

    @staticmethod
    def _read_int(prompt, minimum=None, maximum=None):
        while True:
            raw = input(prompt).strip()
            try:
                val = int(raw)
                if minimum is not None and val < minimum:
                    error(f"Number must be at least {minimum}.")
                    continue
                if maximum is not None and val > maximum:
                    error(f"Number cannot exceed {maximum}.")
                    continue
                return val
            except ValueError:
                error("Please enter a valid integer.")

    @staticmethod
    def _read_index(total_items, prompt):
        if total_items <= 0:
            warning("No records available to select.")
            return None

        while True:
            val = StudentCommandCenter._read_int(prompt, minimum=1, maximum=total_items)
            return val - 1

    @staticmethod
    def _read_date(prompt):
        while True:
            raw = input(prompt).strip()
            try:
                parsed = datetime.strptime(raw, "%Y-%m-%d")
                return parsed.date().isoformat()
            except ValueError:
                error("Invalid date format. Please use YYYY-MM-DD (e.g. 2026-10-15).")
