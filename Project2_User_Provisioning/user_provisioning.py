"""
User Account Provisioning Automation Script
Author: Durgavaraprasad S
Date: February 2026

Purpose: Automate user account creation from CSV files with email validation,
error handling, and logging. Generates output files for successfully processed
users and users with validation errors.

Skills Demonstrated:
- CSV file reading and writing
- Email validation using regular expressions (regex)
- Input validation and error handling
- String manipulation and formatting
- Logging with timestamps
- Functions and modular code organization
- File I/O operations
"""

# Import the csv module to read and write CSV files
# CSV = Comma Separated Values (like Excel but simpler)
import csv

# Import re (regular expressions) for pattern matching (used for email validation)
# Regex is like a search pattern - we use it to check if emails are valid
import re

# Import datetime to add timestamps to our log messages
# This helps track when each action happened
from datetime import datetime

# Import os module for file system operations (checking if files exist, etc.)
import os


def validate_email(email):
    """
    Validate if an email address is in correct format
    Uses regex pattern matching to check email structure
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    # Check if email is None or empty string
    # 'not email' is True when email is None, empty string, or only whitespace
    if not email:
        # Return False because empty emails are not valid
        return False
    
    # Define regex pattern for valid email format
    # This pattern checks: something@something.something
    # ^ means start of string, $ means end of string
    # [a-zA-Z0-9._-]+ means one or more letters, numbers, dots, underscores, or hyphens
    # @ is literal @ symbol (required in all emails)
    # [a-zA-Z0-9.-]+ means domain name (like 'company' or 'gmail')
    # \. means a literal dot (the backslash escapes the special meaning)
    # [a-zA-Z]{2,} means at least 2 letters for extension (like 'com', 'org', 'co.uk')
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.match() tries to match the pattern against the email string
    # If it matches, it returns a match object (which is truthy)
    # If it doesn't match, it returns None (which is falsy)
    # Convert the result to True/False using bool()
    return bool(re.match(pattern, email))


def generate_username(first_name, last_name):
    """
    Generate standardized username from first and last name
    Format: first_initial + last_name (e.g., 'jsmith' for John Smith)
    
    Args:
        first_name (str): User's first name
        last_name (str): User's last name
        
    Returns:
        str: Generated username, or None if names are invalid
    """
    # Check if either name is missing or empty
    # 'not first_name' is True when first_name is None, empty, or whitespace
    if not first_name or not last_name:
        # Return None to indicate we couldn't generate a username
        return None
    
    # .strip() removes whitespace from beginning and end of string
    # For example: "  John  " becomes "John"
    first_name = first_name.strip()
    last_name = last_name.strip()
    
    # Double-check that names aren't empty after removing whitespace
    if not first_name or not last_name:
        return None
    
    # [0] gets the first character of the string
    # .lower() converts the character to lowercase
    # For example: 'John'[0].lower() gives 'j'
    first_initial = first_name[0].lower()
    
    # Convert entire last name to lowercase
    # For example: 'Smith' becomes 'smith'
    last_name_lower = last_name.lower()
    
    # Combine first initial and lowercase last name
    # For example: 'j' + 'smith' = 'jsmith'
    username = first_initial + last_name_lower
    
    # Return the generated username
    return username


def validate_user_data(user):
    """
    Validate all required fields for a user record
    Checks that all necessary fields have values
    
    Args:
        user (dict): Dictionary containing user data from CSV
        
    Returns:
        tuple: (is_valid, error_message)
               is_valid is True/False
               error_message describes what's wrong (or empty string if valid)
    """
    # Create a list of field names that must have values
    # These are the minimum fields needed to create a user account
    required_fields = ['first_name', 'last_name', 'email', 'department', 'role']
    
    # Loop through each required field name
    for field in required_fields:
        # Check if the field exists in the user dictionary AND has a value
        # user.get(field) retrieves the value for that field (returns None if missing)
        # 'not user.get(field)' is True if field is missing or empty
        if not user.get(field):
            # If field is missing/empty, return False and error message
            # Return is a tuple: (False, "error message")
            return False, f"Missing required field: {field}"
    
    # Validate the email address using our validate_email function
    # user['email'] gets the email value from the user dictionary
    if not validate_email(user['email']):
        # If email is invalid, return False with error message
        return False, f"Invalid email format: {user['email']}"
    
    # If we get here, all validations passed!
    # Return True and empty string (no error message)
    return True, ""


def process_users(input_file, success_file='processed_users.csv', error_file='error_users.csv'):
    """
    Process users from input CSV file
    Creates output files for successfully processed users and users with errors
    
    Args:
        input_file (str): Path to input CSV file with user data
        success_file (str): Path to output file for successfully processed users
        error_file (str): Path to output file for users with validation errors
        
    Returns:
        dict: Statistics about processing (counts of success/errors)
    """
    # Create lists to store user records as we process them
    # These are Python lists - we can add items to them with .append()
    successful_users = []  # Will store users who passed validation
    error_users = []       # Will store users who failed validation
    
    # Try to open and read the input file - catch errors if file doesn't exist
    try:
        # open() opens the file in read mode ('r')
        # encoding='utf-8' handles special characters correctly
        # 'with' ensures file closes automatically when done
        with open(input_file, 'r', encoding='utf-8') as file:
            # csv.DictReader reads CSV and converts each row to a dictionary
            # Column headers become dictionary keys, row values become dictionary values
            # For example: {'first_name': 'John', 'last_name': 'Smith', ...}
            reader = csv.DictReader(file)
            
            # Loop through each row in the CSV file
            # 'row' is a dictionary representing one user
            for row in reader:
                # Call validate_user_data to check if this user's data is valid
                # This returns a tuple: (True/False, "error message")
                is_valid, error_message = validate_user_data(row)
                
                # Check if validation passed
                if is_valid:
                    # User is valid! Generate username for them
                    username = generate_username(row['first_name'], row['last_name'])
                    
                    # Add the username to the user's data dictionary
                    row['username'] = username
                    
                    # Add status field to indicate successful processing
                    row['status'] = 'Processed'
                    
                    # .append() adds this user to our successful_users list
                    successful_users.append(row)
                    
                else:
                    # User failed validation - they have errors
                    # Add the error message to their data so we know what went wrong
                    row['error_reason'] = error_message
                    
                    # Mark their status as Error
                    row['status'] = 'Error'
                    
                    # Add this user to our error_users list
                    error_users.append(row)
        
    # Catch the error if input file doesn't exist
    except FileNotFoundError:
        # Print error message
        print(f"✗ Error: Input file '{input_file}' not found.")
        # Return None to indicate failure
        return None
        
    # Catch any other unexpected errors
    except Exception as e:
        # Print the error message
        print(f"✗ Error reading input file: {e}")
        # Return None to indicate failure
        return None
    
    # Write successful users to output file
    # Check if we have any successful users before creating file
    if successful_users:
        # Call helper function to write users to CSV
        write_output_file(success_file, successful_users, include_error_column=False)
        
    # Write error users to output file
    # Check if we have any error users before creating file
    if error_users:
        # Call helper function to write error users to CSV
        # include_error_column=True adds the error_reason column
        write_output_file(error_file, error_users, include_error_column=True)
    
    # Create a dictionary with processing statistics
    # This helps us understand what happened during processing
    stats = {
        'total_processed': len(successful_users),  # How many users succeeded
        'total_errors': len(error_users),          # How many users had errors
        'total_users': len(successful_users) + len(error_users)  # Total users processed
    }
    
    # Return the statistics dictionary
    return stats


def write_output_file(filename, users, include_error_column=False):
    """
    Write user data to CSV output file
    
    Args:
        filename (str): Name of file to create
        users (list): List of user dictionaries to write
        include_error_column (bool): Whether to include error_reason column
    """
    # Try to create and write to the file - catch any errors
    try:
        # open() in write mode ('w') creates new file (overwrites if exists)
        # newline='' prevents extra blank lines in CSV on Windows
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            
            # Define which columns to include in output file
            # These will be the CSV headers
            if include_error_column:
                # For error file: include error_reason column
                fieldnames = ['first_name', 'last_name', 'email', 'department', 'role', 'status', 'error_reason']
            else:
                # For success file: include username instead
                fieldnames = ['first_name', 'last_name', 'email', 'department', 'role', 'username', 'status']
            
            # csv.DictWriter converts dictionaries to CSV rows
            # It needs to know which fields (columns) to write
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header row (column names)
            writer.writeheader()
            
            # Loop through each user dictionary in our list
            for user in users:
                # Write this user as a row in the CSV file
                # DictWriter automatically extracts the right fields from the dictionary
                writer.writerow(user)
        
        # Print success message with filename
        print(f"✓ Output written to: {filename}")
        
    # Catch any errors that occur during file writing
    except Exception as e:
        # Print error message with details
        print(f"✗ Error writing to {filename}: {e}")


def log_action(message, log_file='provisioning.log'):
    """
    Log actions to a log file with timestamp
    Helps track what happened and when
    
    Args:
        message (str): Message to log
        log_file (str): Name of log file
    """
    # Try to write to log file - catch any errors
    try:
        # open() in append mode ('a') adds to end of file without erasing existing content
        # If file doesn't exist, it creates a new one
        with open(log_file, 'a', encoding='utf-8') as file:
            # Get current date and time
            # datetime.now() gets the current moment
            timestamp = datetime.now()
            
            # Format timestamp as string: YYYY-MM-DD HH:MM:SS
            # For example: 2026-02-17 14:30:45
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            # Create log entry: [timestamp] message
            # For example: [2026-02-17 14:30:45] Processing started
            log_entry = f"[{timestamp_str}] {message}\n"
            
            # Write the log entry to the file
            # \n at the end creates a new line for the next log entry
            file.write(log_entry)
            
    # Catch any errors that occur during logging
    # Don't print error because logging failures shouldn't stop the main program
    except Exception as e:
        # Silently pass - logging is not critical
        # In production, you might want to print this error
        pass


def print_summary(stats):
    """
    Print a formatted summary of processing results
    Makes it easy to see what happened at a glance
    
    Args:
        stats (dict): Dictionary containing processing statistics
    """
    # Print a separator line for visual clarity
    print("\n" + "=" * 70)
    
    # Print section header
    print("PROCESSING SUMMARY")
    
    # Print another separator line
    print("=" * 70)
    
    # Print total users processed from stats dictionary
    print(f"Total Users Processed:     {stats['total_users']}")
    
    # Print successful users count
    print(f"Successfully Processed:    {stats['total_processed']}")
    
    # Print error users count
    print(f"Errors Encountered:        {stats['total_errors']}")
    
    # Calculate success percentage
    # Avoid division by zero by checking if total is greater than 0
    if stats['total_users'] > 0:
        # Calculate: (successful / total) * 100
        # :.1f formats number with 1 decimal place
        success_rate = (stats['total_processed'] / stats['total_users']) * 100
        print(f"Success Rate:              {success_rate:.1f}%")
    
    # Print closing separator line
    print("=" * 70 + "\n")


def main():
    """
    Main function to execute user provisioning automation
    This orchestrates the entire process
    """
    # Print welcome banner
    print("\n" + "=" * 70)
    print("USER ACCOUNT PROVISIONING AUTOMATION")
    print("=" * 70 + "\n")
    
    # Define input and output filenames
    # These are the files we'll work with
    input_file = 'new_users.csv'           # File containing new users to process
    success_file = 'processed_users.csv'    # File for successfully processed users
    error_file = 'error_users.csv'          # File for users with errors
    log_file = 'provisioning.log'           # File to log all actions
    
    # Log that processing is starting
    # This creates a record in our log file
    log_action("=== User Provisioning Started ===", log_file)
    
    # Check if input file exists before trying to process it
    # os.path.exists() returns True if file exists, False otherwise
    if not os.path.exists(input_file):
        # Print error message
        print(f"✗ Error: Input file '{input_file}' not found.")
        # Log the error
        log_action(f"ERROR: Input file '{input_file}' not found", log_file)
        # Exit the program - no point continuing without input file
        return
    
    # Print status message to user
    print(f"Processing users from: {input_file}")
    # Log this action
    log_action(f"Processing users from: {input_file}", log_file)
    
    # Call process_users function to do the main work
    # This reads the input file, validates users, and creates output files
    # Returns statistics about what happened
    stats = process_users(input_file, success_file, error_file)
    
    # Check if processing succeeded (stats will be None if it failed)
    if stats is None:
        # Print error message
        print("✗ Processing failed. Check error messages above.")
        # Log the failure
        log_action("ERROR: Processing failed", log_file)
        # Exit the function
        return
    
    # Processing succeeded! Print the summary
    print_summary(stats)
    
    # Log the results
    log_action(f"Successfully processed: {stats['total_processed']} users", log_file)
    log_action(f"Errors encountered: {stats['total_errors']} users", log_file)
    log_action("=== User Provisioning Completed ===", log_file)
    
    # Print completion message
    print("✓ Processing complete!")
    print(f"✓ Log file saved to: {log_file}\n")


# Entry point - this runs when script is executed directly
# __name__ == "__main__" is only True when running this file directly
# (not when importing it as a module in another Python file)
if __name__ == "__main__":
    # Call the main function to start the automation
    main()
