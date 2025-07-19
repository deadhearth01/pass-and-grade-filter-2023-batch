import pandas as pd
import csv

def match_roll_numbers():
    """
    Match roll numbers from column 1 of auth_rows_latest.csv with column 1 of 2023-batch-SEM file
    and create a new CSV with matching rows.
    """
    
    # Read the auth_rows_latest.csv file
    print("Reading auth_rows_latest.csv...")
    auth_df = pd.read_csv('Auth_rows_latest.csv')
    
    # Read the 2023-batch-SEM file
    print("Reading 2023-batch-SEM file...")
    batch_df = pd.read_csv('2023-batch-SEM 1-4_Results + Details - Details of the students  + Results.csv')
    
    # Get roll numbers from auth file (column 1 - "rollNo")
    auth_roll_numbers = set(auth_df['rollNo'].astype(str))
    print(f"Found {len(auth_roll_numbers)} unique roll numbers in auth file")
    
    # Get roll numbers from batch file (column 1 - "Registration no")
    batch_roll_numbers = set(batch_df['Registration no'].astype(str))
    print(f"Found {len(batch_roll_numbers)} unique roll numbers in batch file")
    
    # Find matching roll numbers
    matching_roll_numbers = auth_roll_numbers.intersection(batch_roll_numbers)
    print(f"Found {len(matching_roll_numbers)} matching roll numbers")
    
    # Find missing roll numbers (in auth but not in batch)
    missing_roll_numbers = auth_roll_numbers - batch_roll_numbers
    print(f"Found {len(missing_roll_numbers)} roll numbers from auth file that are missing in batch file")
    
    # Filter batch file to only include matching rows
    matching_rows = batch_df[batch_df['Registration no'].astype(str).isin(matching_roll_numbers)]
    
    # Save matching rows to a new CSV file
    output_filename = 'matching_students.csv'
    matching_rows.to_csv(output_filename, index=False)
    
    print(f"Saved {len(matching_rows)} matching rows to {output_filename}")
    
    # Save missing roll numbers to a file
    missing_filename = 'missing_roll_numbers.csv'
    with open(missing_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Missing Roll Numbers from Auth File'])
        for roll_no in sorted(missing_roll_numbers):
            writer.writerow([roll_no])
    
    print(f"Saved missing roll numbers to {missing_filename}")
    
    # Also create a summary file with just the matching roll numbers
    summary_filename = 'matching_roll_numbers_summary.csv'
    with open(summary_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Matching Roll Numbers'])
        for roll_no in sorted(matching_roll_numbers):
            writer.writerow([roll_no])
    
    print(f"Saved summary of matching roll numbers to {summary_filename}")
    
    # Print some statistics
    print(f"\nStatistics:")
    print(f"Total roll numbers in auth file: {len(auth_roll_numbers)}")
    print(f"Total roll numbers in batch file: {len(batch_roll_numbers)}")
    print(f"Matching roll numbers: {len(matching_roll_numbers)}")
    print(f"Missing roll numbers: {len(missing_roll_numbers)}")
    print(f"Match percentage: {(len(matching_roll_numbers) / len(auth_roll_numbers) * 100):.2f}%")
    
    # Print first few matching roll numbers for verification
    print(f"\nFirst 10 matching roll numbers:")
    for i, roll_no in enumerate(sorted(matching_roll_numbers)[:10]):
        print(f"{i+1}. {roll_no}")
    
    # Print missing roll numbers
    print(f"\nMissing roll numbers (in auth but not in batch):")
    for i, roll_no in enumerate(sorted(missing_roll_numbers)):
        print(f"{i+1}. {roll_no}")
    
    # Verify by checking a few specific roll numbers
    print(f"\nVerification - Checking a few roll numbers:")
    sample_auth_rolls = list(auth_roll_numbers)[:5]
    for roll_no in sample_auth_rolls:
        in_batch = roll_no in batch_roll_numbers
        print(f"Roll {roll_no}: {'✓ Found' if in_batch else '✗ Missing'} in batch file")
    
    return matching_rows, missing_roll_numbers

if __name__ == "__main__":
    try:
        result, missing = match_roll_numbers()
        print("\nScript completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
