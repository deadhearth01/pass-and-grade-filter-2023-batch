import csv
from collections import defaultdict

# Define custom grade order (lowest to highest)
GRADE_ORDER = ['F', 'R', 'P', 'C', 'B', 'B+', 'A', 'A+', 'O']
GRADE_RANK = {grade: i for i, grade in enumerate(GRADE_ORDER)}

def get_grade_rank(grade):
    return GRADE_RANK.get(grade, len(GRADE_ORDER))  # Unknown grades go last

# Read student details into a dict
student_details = {}
with open('purchased_students_details.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_details[row['Registration no']] = row

# Read matched courses and collect rows
matched_rows = []
with open('matched_courses_detailed.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        matched_rows.append(row)

# Sort matched rows by grade (lowest first)
matched_rows.sort(key=lambda x: get_grade_rank(x['grade']))

# Prepare output fieldnames
# Combine all fields from matched_courses_detailed and purchased_students_details
sample_student = next(iter(student_details.values()))
output_fieldnames = list(matched_rows[0].keys()) + [k for k in sample_student.keys() if k != 'Registration no']

# Write output CSV
with open('sorted_courses_with_details.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=output_fieldnames)
    writer.writeheader()
    for row in matched_rows:
        reg_no = row['roll_no']
        details = student_details.get(reg_no, {})
        combined = dict(row)
        for k, v in details.items():
            if k != 'Registration no':
                combined[k] = v
        writer.writerow(combined)

print('Done. Output written to sorted_courses_with_details.csv') 