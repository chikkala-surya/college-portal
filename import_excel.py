import pandas as pd
import sqlite3

conn = sqlite3.connect("college.db")

# =========================
# STUDENT TABLES
# =========================


pd.read_excel(
    "excel_data/login.xlsx"
).to_sql(
    "student_login",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/attendance.xlsx"
).to_sql(
    "attendance",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/internal_marks.xlsx"
).to_sql(
    "internal_marks",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/external_marks.xlsx"
).to_sql(
    "external_marks",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/semester_results.xlsx"
).to_sql(
    "semester_results",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/fee_details.xlsx"
).to_sql(
    "fee_details",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/timetable.xlsx"
).to_sql(
    "timetable",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/backlog.xlsx"
).to_sql(
    "backlogs",
    conn,
    if_exists="replace",
    index=False
)

# =========================
# FACULTY TABLES
# =========================

pd.read_excel(
    "excel_data/faculty_login.xlsx"
).to_sql(
    "faculty_login",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/events.xlsx"
).to_sql(
    "events",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/library_books.xlsx"
).to_sql(
    "library_books",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/placement_drives.xlsx"
).to_sql(
    "placement_drives",
    conn,
    if_exists="replace",
    index=False
)

# =========================
# EXTRA MODULES
# =========================

pd.read_excel(
    "excel_data/achievements.xlsx"
).to_sql(
    "achievements",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/assignments.xlsx"
).to_sql(
    "assignments",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/certificates.xlsx"
).to_sql(
    "certificates",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/clubs.xlsx"
).to_sql(
    "clubs",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/student_clubs.xlsx"
).to_sql(
    "student_clubs",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/exam_schedule.xlsx"
).to_sql(
    "exam_schedule",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/hostel_details.xlsx"
).to_sql(
    "hostel_details",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/issued_books.xlsx"
).to_sql(
    "issued_books",
    conn,
    if_exists="replace",
    index=False
)

pd.read_excel(
    "excel_data/leave_requests.xlsx"
).to_sql(
    "leave_requests",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("=" * 50)
print("ALL EXCEL FILES IMPORTED SUCCESSFULLY")
print("DATABASE CREATED: college.db")
print("=" * 50)