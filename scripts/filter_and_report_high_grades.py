import csv
import os
from collections import defaultdict

# Output directory
OUTPUT_DIR = 'grade_filtered'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the sorted file
with open('sorted_courses_with_details.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Group by grade
grade_groups = defaultdict(list)
for row in rows:
    grade_groups[row['grade']].append(row)

# Write O-grade students to one file
with open(os.path.join(OUTPUT_DIR, 'O_grade_students.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    for row in grade_groups.get('O', []):
        writer.writerow(row)

# Write other grades to separate files
for grade, group in grade_groups.items():
    if grade == 'O':
        continue
    filename = f'{grade}_grade_students.csv'
    with open(os.path.join(OUTPUT_DIR, filename), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in group:
            writer.writerow(row)

# Collect unique students with O or similar grades (A+, O)
high_grades = {'O', 'A+'}
high_grade_students = {}
for grade in high_grades:
    for row in grade_groups.get(grade, []):
        high_grade_students[row['roll_no']] = row
with open(os.path.join(OUTPUT_DIR, 'high_grade_students.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    for row in high_grade_students.values():
        writer.writerow(row)

# Generate markdown report
report_lines = ['# Grade Report for Feedback Contact\n']
for grade in sorted(grade_groups.keys(), key=lambda g: ['F','R','P','C','B','B+','A','A+','O'].index(g) if g in ['F','R','P','C','B','B+','A','A+','O'] else 99):
    report_lines.append(f'\n## Grade: {grade}\n')
    for row in grade_groups[grade]:
        report_lines.append(f"- {row['roll_no']} | {row.get('Name','')} | {row.get('Email','')} | {row.get('Student Mobile','')} | {row.get('Parent Mobile','')}")
with open(os.path.join(OUTPUT_DIR, 'grade_report.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print('Filtering and report generation complete. See grade_filtered folder.') 