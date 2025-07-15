# Pass Percentage Analysis Report

## Overview
This report presents a detailed analysis of the pass percentage for students who purchased specific courses, based on data from `Auth_rows_latest.csv` and `matching_students.csv`. The analysis matches course IDs from the auth file with the sem4 courses in the student file, extracts grades, and calculates pass percentages.

---

## Methodology
1. **Data Sources:**
   - `Auth_rows_latest.csv`: Contains student roll numbers and the list of course IDs they purchased.
   - `matching_students.csv`: Contains detailed student records, including all semester courses and grades.
2. **Matching Logic:**
   - For each student in the auth file, find the corresponding student in the matching file by roll number.
   - Extract the `sem4_courses` field for that student.
   - Parse the course IDs from the auth file and match them to the course codes in `sem4_courses`.
   - Extract the grade for each matched course.
3. **Pass Criteria:**
   - Grades considered as pass: `A+`, `A`, `B+`, `B`, `C+`, `C`, `D+`, `D`, `S`, `O`, `P`.
   - Grades considered as fail: `F`, `R` (as per the data, but you can adjust as needed).
4. **Analysis Outputs:**
   - Overall pass percentage
   - Course-wise pass percentage
   - Grade distribution
   - Student-wise pass summary

---

## Results

### Overall Pass Percentage
| Metric            | Value   |
|-------------------|---------|
| Total Courses     | 369     |
| Passed Courses    | 340     |
| Failed Courses    | 29      |
| Pass Percentage   | 92.14%  |

### Course-wise Pass Percentage
| Course Code | Total Students | Passed Students | Pass Percentage |
|-------------|---------------|----------------|-----------------|
| CSEN1101    | 77            | 75             | 97.4%           |
| CSEN2011    | 111           | 104            | 93.7%           |
| CSEN2021    | 99            | 96             | 97.0%           |
| CSEN3151    | 15            | 15             | 100.0%          |
| MATH2361    | 67            | 50             | 74.6%           |

### Grade Distribution
| Grade | Count |
|-------|-------|
| A+    | 32    |
| A     | 52    |
| B+    | 145   |
| B     | 53    |
| C     | 26    |
| O     | 27    |
| P     | 5     |
| F     | 28    |
| R     | 1     |

---

## Key Insights
- **High Pass Rate:** The overall pass percentage for students who purchased these courses is **92.14%**.
- **Strong Performance in CS Courses:** Most computer science courses (CSEN1101, CSEN2011, CSEN2021, CSEN3151) have pass rates above 93%, with CSEN3151 at 100%.
- **Challenging Math Course:** MATH2361 has the lowest pass rate at 74.6%.
- **Grade Distribution:** The majority of students scored in the `B+` and `B` range, with a small number failing (`F` or `R`).
- **Grade 'P' is now considered a pass, as per updated criteria.**

---

## Files Generated
- `matched_courses_detailed.csv`: Detailed student-course-grade data
- `course_pass_percentage_summary.csv`: Course-wise summary
- `student_pass_percentage_summary.csv`: Student-wise summary
- `overall_pass_percentage_summary.csv`: Overall summary

---

## How to Reproduce
1. Run `python3 pass_percentage_analyzer.py` in your project directory.
2. The script will generate all summary and detailed files listed above.
3. Review this markdown file for a human-readable summary of the results.

---

*Analysis performed automatically using Python and pandas. For questions or further breakdowns, please contact the data analyst.* 