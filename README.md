# VIT Student Command Center

## Introduction
The VIT Student Command Center is a Python-based desktop command-line application designed to help students manage their academic, personal, and daily responsibilities in one place. The project was created to simplify routine student tasks such as tracking marks, managing assignments, monitoring attendance, planning study sessions, and recording expenses.

Instead of keeping information in multiple places, students can use this system to maintain a centralized record of their work and progress. The project is simple, easy to use, and built using Python’s built-in features without requiring any external libraries.

## Problem Statement
Students often struggle to keep track of multiple activities at the same time. Academic performance, assignment deadlines, attendance, and expenses are all important, but they are usually managed separately. This creates confusion and often leads to missed deadlines or poor planning.

This project addresses that issue by creating a single application where these tasks can be recorded and updated efficiently.

## Objectives
The main objectives of the project are:
- to build a student management system that is easy to use,
- to keep track of academic performance,
- to manage assignments and due dates,
- to monitor attendance percentages,
- to record and analyze expenses,
- to maintain a structured study plan,
- to store data safely between sessions.

## Scope
The project focuses on a terminal-based student utility that handles core academic and personal tracking features. The system is meant to be lightweight and practical for individual student use.

## Features
- Student dashboard with overview information
- Subject-wise academic score tracking
- Grade calculation based on marks
- Assignment add, complete, and delete options
- Expense recording and category tracking
- Attendance percentage calculation
- Study task planner and progress tracking
- Editable student profile
- JSON-based persistent data storage
- Menu-driven interface with validation

## Tools and Technologies
- Python
- Dataclasses
- JSON file handling
- Standard library modules
- Terminal-based user interface

## Project Structure
```text
VIT Student Command Center/
├── app.py
├── main.py
├── models.py
├── storage.py
├── ui.py
├── README.md
├── data/
│   ├── assignments.json
│   ├── expenses.json
│   ├── student.json
│   ├── study_tasks.json
│   └── subjects.json
```

## How to Run
Open the project folder in the terminal and run:

```bash
python3 main.py
```

## Module Description

### 1. Student Model
This part defines the student details such as name, registration number, semester, and branch.

### 2. Subject Model
This stores subject names, marks obtained, total marks, and attendance percentage for each subject.

### 3. Assignment Module
This section allows the user to keep track of assignment titles, subject names, due dates, and completion status.

### 4. Expense Tracker
This feature stores expense records including category, amount, note, and date. It helps students understand where their money is being spent.

### 5. Study Planner
This module keeps a list of academic tasks along with subject, topic, estimated time, and completion status.

### 6. Storage System
The application stores all data in JSON files so that users do not lose their information after closing the program.

## Advantages
- simple and easy to understand,
- no external dependencies,
- fast and lightweight,
- helpful for personal academic tracking,
- easy to modify and expand.

## Limitations
- command-line based interface only,
- no advanced reporting or chart generation,
- no multi-user support,
- limited database capabilities compared to larger systems.

## Future Improvements
- add a graphical user interface,
- include charts and analytics,
- add filters and report generation,
- support data export to CSV,
- add user authentication for multiple students.

## Conclusion
The VIT Student Command Center is a practical student management project that brings together academic tracking, planning, attendance analysis, and expense monitoring in a single application. It is lightweight, easy to use, and suitable for academic demonstration as well as personal productivity use.

This project reflects a clear understanding of Python programming and structured application design while solving a real-world problem faced by students in day-to-day academic life.

## License
This project is intended for educational and personal use.

