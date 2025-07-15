import pandas as pd
import re
import json

def parse_sem4_courses(sem4_courses_str):
    """
    Parse sem4_courses string to extract course codes and grades
    Format: "CSEN1101:Operating Systems:Theory/Practical:4:A+:April:2025"
    Returns: list of tuples (course_code, grade)
    """
    if pd.isna(sem4_courses_str) or sem4_courses_str == '':
        return []
    
    courses = []
    # Split by semicolon to get individual courses
    course_list = sem4_courses_str.split(';')
    
    for course in course_list:
        if course.strip():
            # Split by colon to get course parts
            parts = course.split(':')
            if len(parts) >= 5:
                course_code = parts[0].strip()
                # Grade is the 5th part (index 4) - after the credits
                grade = parts[4].strip()
                courses.append((course_code, grade))
    
    return courses

def extract_course_ids_from_auth(course_ids_str):
    """
    Extract course IDs from the courseIds column in auth file
    Format: '["MATH2361","CSEN3151","CSEN2011","CSEN2021"]'
    """
    if pd.isna(course_ids_str) or course_ids_str == '':
        return []
    
    try:
        # Parse the JSON-like string
        course_ids = json.loads(course_ids_str)
        return [str(course_id).strip() for course_id in course_ids]
    except:
        # If JSON parsing fails, try to extract manually
        # Remove brackets and quotes, split by comma
        cleaned = course_ids_str.replace('[', '').replace(']', '').replace('"', '')
        course_ids = [course.strip() for course in cleaned.split(',') if course.strip()]
        return course_ids

def analyze_pass_percentage():
    """
    Analyze pass percentage by matching course IDs from auth file with sem4 courses
    """
    print("Reading files...")
    
    # Read the files
    auth_df = pd.read_csv('Auth_rows_latest.csv')
    matching_df = pd.read_csv('matching_students.csv')
    
    print(f"Auth file has {len(auth_df)} rows")
    print(f"Matching students file has {len(matching_df)} rows")
    
    # Create a dictionary to store results
    results = []
    all_matched_courses = []
    
    # Process each row in auth file
    for idx, auth_row in auth_df.iterrows():
        roll_no = str(auth_row['rollNo'])
        
        # Find corresponding student in matching file
        matching_student = matching_df[matching_df['Registration no'].astype(str) == roll_no]
        
        if len(matching_student) == 0:
            print(f"Warning: Roll number {roll_no} not found in matching students file")
            continue
        
        # Get sem4_courses for this student
        sem4_courses_str = matching_student.iloc[0]['sem4_courses']
        sem4_courses = parse_sem4_courses(sem4_courses_str)
        
        # Get course IDs from auth file
        auth_course_ids = extract_course_ids_from_auth(auth_row['courseIds'])
        
        # Find matching courses
        matching_courses = []
        for course_code, grade in sem4_courses:
            if course_code in auth_course_ids:
                matching_courses.append({
                    'roll_no': roll_no,
                    'course_code': course_code,
                    'grade': grade,
                    'course_name': course_code  # We can extract full name if needed
                })
                all_matched_courses.append({
                    'roll_no': roll_no,
                    'course_code': course_code,
                    'grade': grade
                })
        
        # Store results for this student
        if matching_courses:
            results.append({
                'roll_no': roll_no,
                'matching_courses': matching_courses,
                'total_matching_courses': len(matching_courses)
            })
    
    # Convert to DataFrame for easier analysis
    if all_matched_courses:
        matched_courses_df = pd.DataFrame(all_matched_courses)
        
        # Define pass grades (you can modify this based on your institution's criteria)
        pass_grades = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'S', 'O', 'P']
        
        # Calculate pass percentage
        total_courses = len(matched_courses_df)
        passed_courses = len(matched_courses_df[matched_courses_df['grade'].isin(pass_grades)])
        pass_percentage = (passed_courses / total_courses * 100) if total_courses > 0 else 0
        
        # Save detailed results
        matched_courses_df.to_csv('matched_courses_detailed.csv', index=False)
        
        # Create summary by course
        course_summary = matched_courses_df.groupby('course_code').agg({
            'grade': ['count', lambda x: sum(x.isin(pass_grades))]
        }).round(2)
        course_summary.columns = ['total_students', 'passed_students']
        course_summary['pass_percentage'] = (course_summary['passed_students'] / course_summary['total_students'] * 100).round(2)
        course_summary.to_csv('course_pass_percentage_summary.csv')
        
        # Create summary by student
        student_summary = matched_courses_df.groupby('roll_no').agg({
            'grade': ['count', lambda x: sum(x.isin(pass_grades))]
        }).round(2)
        student_summary.columns = ['total_courses', 'passed_courses']
        student_summary['pass_percentage'] = (student_summary['passed_courses'] / student_summary['total_courses'] * 100).round(2)
        student_summary.to_csv('student_pass_percentage_summary.csv')
        
        # Print results
        print(f"\n=== PASS PERCENTAGE ANALYSIS ===")
        print(f"Total matched courses: {total_courses}")
        print(f"Passed courses: {passed_courses}")
        print(f"Failed courses: {total_courses - passed_courses}")
        print(f"Overall pass percentage: {pass_percentage:.2f}%")
        
        print(f"\n=== COURSE-WISE BREAKDOWN ===")
        for course_code in matched_courses_df['course_code'].unique():
            course_data = matched_courses_df[matched_courses_df['course_code'] == course_code]
            course_total = len(course_data)
            course_passed = len(course_data[course_data['grade'].isin(pass_grades)])
            course_pass_percent = (course_passed / course_total * 100) if course_total > 0 else 0
            print(f"{course_code}: {course_passed}/{course_total} ({course_pass_percent:.1f}%)")
        
        print(f"\n=== GRADE DISTRIBUTION ===")
        grade_counts = matched_courses_df['grade'].value_counts().sort_index()
        for grade, count in grade_counts.items():
            print(f"{grade}: {count}")
        
        # Save overall summary
        summary_data = {
            'metric': ['Total Courses', 'Passed Courses', 'Failed Courses', 'Pass Percentage'],
            'value': [total_courses, passed_courses, total_courses - passed_courses, f"{pass_percentage:.2f}%"]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv('overall_pass_percentage_summary.csv', index=False)
        
        return matched_courses_df, pass_percentage
        
    else:
        print("No matching courses found!")
        return None, 0

if __name__ == "__main__":
    try:
        matched_courses, pass_percentage = analyze_pass_percentage()
        print("\nScript completed successfully!")
        print(f"Files created:")
        print("- matched_courses_detailed.csv (detailed course-wise data)")
        print("- course_pass_percentage_summary.csv (course-wise summary)")
        print("- student_pass_percentage_summary.csv (student-wise summary)")
        print("- overall_pass_percentage_summary.csv (overall summary)")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc() 