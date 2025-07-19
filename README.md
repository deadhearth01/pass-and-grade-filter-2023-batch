# GITAM Pass Percentage Analysis Project

## Project Structure

```
pass---2023-batch/
│
├── data_raw/                # All original/raw CSVs (student, course, and result data)
├── scripts/                 # All Python scripts for processing and analysis
├── results/                 # All generated/processed files
│   └── grade_filtered/      # All grade-based filtered outputs and reports
├── docs/                    # Documentation/markdown files
└── README.md                # (This file)
```

---

## Folder Contents

### `data_raw/`
- **Purpose:** Stores all original, unmodified CSV files used as input for analysis.
- **Files:**
  - `matched_courses_detailed.csv` — Course-wise grades for students.
  - `purchased_students_details.csv` — Student details (email, phone, etc.).
  - `student_pass_percentage_summary.csv`, `overall_pass_percentage_summary.csv`, `course_pass_percentage_summary.csv` — Various summaries.
  - `missing_roll_numbers.csv`, `matching_students.csv`, `matching_roll_numbers_summary.csv` — Roll number matching and summary files.
  - `Auth_rows_latest.csv`, `2023-batch-SEM 1-4_Results + Details - Details of the students  + Results.csv` — Other raw data.

### `scripts/`
- **Purpose:** Contains all Python scripts for data processing and analysis.
- **Files:**
  - `filter_and_report_high_grades.py` — Filters students by grade, generates grade-based CSVs and a markdown report. **Input:** `data_raw/` files. **Output:** `results/grade_filtered/`.
  - `sort_grades_with_details.py` — Sorts students by grade and merges with student details. **Input:** `data_raw/` files. **Output:** `results/sorted_courses_with_details.csv`.
  - `reg-match-find.py`, `pass_percentage_analyzer.py` — Other analysis or utility scripts.

### `results/`
- **Purpose:** Stores all processed and output files.
- **Files:**
  - `sorted_courses_with_details.csv` (if present)
  - **Subfolder:** `grade_filtered/`
    - `O_grade_students.csv`, `A+_grade_students.csv`, `A_grade_students.csv`, etc. — Students filtered by grade.
    - `high_grade_students.csv` — All unique students with O or A+ grades.
    - `grade_report.md` — Markdown report listing all students by grade, with contact details.

### `docs/`
- **Purpose:** Documentation and markdown files.
- **Files:**
  - `PASS_PERCENTAGE_ANALYSIS.md` — Project analysis and notes.

---

## How to Use

1. **Raw data** goes in `data_raw/`.
2. **Run scripts** from the `scripts/` folder.  
   - Scripts expect input from `data_raw/` and output to `results/`.
3. **Check results** in `results/` and `results/grade_filtered/`.
4. **Documentation** is in `docs/`.

---

## Contacting High-Grade Students

- Use `results/grade_filtered/O_grade_students.csv` and `A+_grade_students.csv` for top performers.
- The `grade_report.md` in the same folder lists all students by grade, with contact details for easy reference.

---

## Notes
- All temporary or log files should be deleted after use.
- Only `.md` files are used for documentation.
- If you add new scripts or data, update this README accordingly. 