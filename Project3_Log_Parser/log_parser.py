"""
System Health Monitor - Log File Parser
Author: Durgavaraprasad S
Date: February 2026

Purpose: Parse system log files to identify and categorize errors, generate 
summary reports with error counts by severity, find the most frequent error 
messages, and create a timeline of when errors occurred.

Skills Demonstrated:
- Text file processing and parsing
- Regular expressions (regex) for pattern matching
- Dictionary data structures for counting and aggregating
- List operations and sorting
- String manipulation and formatting
- Functions with clear responsibilities
- Error handling for file operations
- Data analysis and reporting
"""

# Import re (regular expressions) for pattern matching in log lines
# Regex lets us find patterns in text, like dates, times, severity levels
import re

# Import Counter from collections for efficient counting of items
# Counter is like a dictionary but optimized for counting things
from collections import Counter

# Import datetime to work with dates and times
from datetime import datetime


def parse_log_line(line):
    """
    Parse a single log line and extract its components
    Expected format: YYYY-MM-DD HH:MM:SS SEVERITY Message text
    
    Args:
        line (str): A single line from the log file
        
    Returns:
        dict: Dictionary with parsed components (timestamp, severity, message)
              Returns None if line doesn't match expected format
    """
    # Regular expression pattern to match log line format
    # Breaking down the pattern:
    # (\d{4}-\d{2}-\d{2}) - Captures date: 4 digits, dash, 2 digits, dash, 2 digits (YYYY-MM-DD)
    # \s+ - Matches one or more whitespace characters (space between date and time)
    # (\d{2}:\d{2}:\d{2}) - Captures time: 2 digits, colon, 2 digits, colon, 2 digits (HH:MM:SS)
    # \s+ - Matches whitespace between time and severity
    # (INFO|WARNING|ERROR|CRITICAL) - Captures severity level (one of these four words)
    # \s+ - Matches whitespace between severity and message
    # (.+) - Captures the rest of the line as the message (. means any character, + means one or more)
    pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(INFO|WARNING|ERROR|CRITICAL)\s+(.+)'
    
    # Try to match the pattern against the line
    # re.match() attempts to match pattern at the beginning of the string
    match = re.match(pattern, line)
    
    # Check if we found a match
    if match:
        # .groups() returns all captured groups from the regex as a tuple
        # Unpack the tuple into individual variables
        date, time, severity, message = match.groups()
        
        # Combine date and time strings: "2026-02-17" + " " + "08:00:15"
        timestamp_str = f"{date} {time}"
        
        # Return a dictionary with all the parsed components
        # This makes it easy to access individual parts later
        return {
            'timestamp': timestamp_str,  # Full timestamp as string
            'date': date,                # Just the date part
            'time': time,                # Just the time part
            'severity': severity,        # Severity level (INFO, WARNING, etc.)
            'message': message.strip()   # Message text (.strip() removes extra whitespace)
        }
    
    # If pattern didn't match, return None to indicate parsing failed
    return None


def read_log_file(filename):
    """
    Read and parse entire log file
    
    Args:
        filename (str): Path to log file
        
    Returns:
        list: List of parsed log entry dictionaries
              Returns None if file cannot be read
    """
    # Create an empty list to store all parsed log entries
    # We'll add each parsed line to this list
    log_entries = []
    
    # Try to open and read the file - catch errors if file doesn't exist
    try:
        # open() opens the file in read mode ('r')
        # encoding='utf-8' handles special characters correctly
        # 'with' ensures file closes automatically even if error occurs
        with open(filename, 'r', encoding='utf-8') as file:
            # Loop through each line in the file
            # file is iterable - each iteration gives us one line
            for line in file:
                # .strip() removes whitespace (including newline character) from beginning and end
                line = line.strip()
                
                # Check if line is not empty (skip blank lines)
                if line:
                    # Call parse_log_line to extract components from this line
                    # This returns a dictionary or None
                    parsed = parse_log_line(line)
                    
                    # Check if parsing was successful (parsed is not None)
                    if parsed:
                        # Add this parsed entry to our list
                        # .append() adds an item to the end of a list
                        log_entries.append(parsed)
        
        # Print success message with count of entries found
        # len(log_entries) tells us how many items are in the list
        print(f"✓ Successfully parsed {len(log_entries)} log entries\n")
        
        # Return the list of all parsed entries
        return log_entries
        
    # Catch the error if file doesn't exist
    except FileNotFoundError:
        # Print error message
        print(f"✗ Error: Log file '{filename}' not found.")
        # Return None to indicate failure
        return None
        
    # Catch any other unexpected errors
    except Exception as e:
        # Print error with details
        print(f"✗ Error reading log file: {e}")
        # Return None to indicate failure
        return None


def count_by_severity(log_entries):
    """
    Count how many log entries exist for each severity level
    
    Args:
        log_entries (list): List of parsed log entry dictionaries
        
    Returns:
        dict: Dictionary with severity levels as keys and counts as values
    """
    # Create a dictionary to store counts for each severity level
    # Initialize each severity with count of 0
    severity_counts = {
        'INFO': 0,
        'WARNING': 0,
        'ERROR': 0,
        'CRITICAL': 0
    }
    
    # Loop through each log entry in our list
    for entry in log_entries:
        # Get the severity level from this entry's dictionary
        # entry['severity'] retrieves the value for the 'severity' key
        severity = entry['severity']
        
        # Increment the count for this severity level
        # severity_counts[severity] gets current count
        # += 1 adds one to it
        # For example: if severity is 'ERROR', this does: severity_counts['ERROR'] += 1
        severity_counts[severity] += 1
    
    # Return the dictionary with all counts
    return severity_counts


def get_error_messages(log_entries):
    """
    Extract all ERROR and CRITICAL messages
    Filter out INFO and WARNING to focus on problems
    
    Args:
        log_entries (list): List of parsed log entry dictionaries
        
    Returns:
        list: List of error message strings
    """
    # Create empty list to store error messages
    error_messages = []
    
    # Loop through each log entry
    for entry in log_entries:
        # Check if severity is either ERROR or CRITICAL
        # 'in' checks if value exists in the list/tuple
        if entry['severity'] in ['ERROR', 'CRITICAL']:
            # This is an error! Get the message text
            # entry['message'] retrieves the message string
            message = entry['message']
            
            # Add this message to our list
            error_messages.append(message)
    
    # Return list of all error messages
    return error_messages


def find_most_frequent_errors(error_messages, top_n=5):
    """
    Find the most frequently occurring error messages
    
    Args:
        error_messages (list): List of error message strings
        top_n (int): Number of top errors to return (default 5)
        
    Returns:
        list: List of tuples (message, count) sorted by frequency
    """
    # Counter is a special dictionary that counts how many times each item appears
    # For example: Counter(['a', 'b', 'a']) gives {'a': 2, 'b': 1}
    error_counter = Counter(error_messages)
    
    # .most_common(n) returns the n most frequent items as a list of tuples
    # Each tuple is (item, count), sorted by count in descending order
    # For example: [('Database timeout', 3), ('API error', 2), ...]
    most_common = error_counter.most_common(top_n)
    
    # Return the list of most common errors
    return most_common


def get_errors_by_hour(log_entries):
    """
    Group errors by hour of the day to identify peak error times
    
    Args:
        log_entries (list): List of parsed log entry dictionaries
        
    Returns:
        dict: Dictionary with hour (0-23) as key and count as value
    """
    # Create dictionary to store error counts for each hour (0-23)
    # Initialize all 24 hours with count of 0
    # This is a dictionary comprehension - compact way to create dictionaries
    # {hour: 0 for hour in range(24)} creates {0: 0, 1: 0, 2: 0, ..., 23: 0}
    hourly_errors = {hour: 0 for hour in range(24)}
    
    # Loop through each log entry
    for entry in log_entries:
        # Only count ERROR and CRITICAL entries, skip INFO and WARNING
        if entry['severity'] in ['ERROR', 'CRITICAL']:
            # Get the time string from entry (format: "HH:MM:SS")
            time_str = entry['time']
            
            # Split the time string by colon to get [hours, minutes, seconds]
            # "08:15:30".split(':') gives ["08", "15", "30"]
            # [0] gets the first element (hours)
            hour_str = time_str.split(':')[0]
            
            # Convert hour string to integer
            # int("08") gives 8
            hour = int(hour_str)
            
            # Increment the count for this hour
            # hourly_errors[8] += 1 adds one to the count for 8:00 AM hour
            hourly_errors[hour] += 1
    
    # Return dictionary with error counts by hour
    return hourly_errors


def generate_summary_report(log_entries):
    """
    Generate and print comprehensive summary report
    
    Args:
        log_entries (list): List of parsed log entry dictionaries
    """
    # Print section header with separator line
    print("=" * 70)
    print("SYSTEM HEALTH MONITOR - LOG ANALYSIS REPORT")
    print("=" * 70 + "\n")
    
    # === SECTION 1: Overall Statistics ===
    print("=" * 70)
    print("OVERALL STATISTICS")
    print("=" * 70)
    
    # len(log_entries) counts total number of log entries
    print(f"Total Log Entries:         {len(log_entries)}")
    
    # Get severity counts by calling our function
    severity_counts = count_by_severity(log_entries)
    
    # Print count for each severity level
    # Access each count using dictionary keys
    print(f"INFO entries:              {severity_counts['INFO']}")
    print(f"WARNING entries:           {severity_counts['WARNING']}")
    print(f"ERROR entries:             {severity_counts['ERROR']}")
    print(f"CRITICAL entries:          {severity_counts['CRITICAL']}")
    
    # Calculate total errors (ERROR + CRITICAL combined)
    total_errors = severity_counts['ERROR'] + severity_counts['CRITICAL']
    print(f"\nTotal Errors/Critical:     {total_errors}")
    
    # Calculate error percentage
    # Avoid division by zero by checking if we have any log entries
    if len(log_entries) > 0:
        # Calculate: (total_errors / total_entries) * 100
        # :.2f formats number with 2 decimal places
        error_percentage = (total_errors / len(log_entries)) * 100
        print(f"Error Rate:                {error_percentage:.2f}%")
    
    # Print blank line for spacing
    print()
    
    # === SECTION 2: Most Frequent Errors ===
    print("=" * 70)
    print("TOP 5 MOST FREQUENT ERRORS")
    print("=" * 70)
    
    # Get all error messages (ERROR and CRITICAL only)
    error_messages = get_error_messages(log_entries)
    
    # Find the 5 most common error messages
    top_errors = find_most_frequent_errors(error_messages, top_n=5)
    
    # Check if we found any errors
    if top_errors:
        # Loop through each error in the top errors list
        # enumerate() gives us both the index and the item
        # start=1 makes the index start at 1 instead of 0
        for index, (message, count) in enumerate(top_errors, start=1):
            # Print: rank. message (occurred X times)
            print(f"{index}. {message} (occurred {count} times)")
    else:
        # No errors found
        print("No errors found in log file.")
    
    # Print blank line
    print()
    
    # === SECTION 3: Errors by Hour ===
    print("=" * 70)
    print("ERROR DISTRIBUTION BY HOUR")
    print("=" * 70)
    
    # Get error counts grouped by hour
    hourly_errors = get_errors_by_hour(log_entries)
    
    # Loop through each hour (0-23)
    for hour in range(24):
        # Get the error count for this hour
        count = hourly_errors[hour]
        
        # Only print hours that had errors (skip hours with 0 errors)
        if count > 0:
            # Format hour as 2-digit string with leading zero if needed
            # f"{hour:02d}" formats 8 as "08", 14 stays "14"
            # Create visual bar using asterisks (* symbols)
            # '*' * count creates a string with 'count' number of asterisks
            # For example: '*' * 3 gives '***'
            bar = '*' * count
            
            # Print: HH:00 - visual bar (count errors)
            print(f"{hour:02d}:00 - {bar} ({count} errors)")
    
    # Print blank line
    print()
    
    # === SECTION 4: Critical Events ===
    print("=" * 70)
    print("CRITICAL EVENTS TIMELINE")
    print("=" * 70)
    
    # Create empty list to store just the CRITICAL entries
    critical_events = []
    
    # Loop through all log entries
    for entry in log_entries:
        # Check if this is a CRITICAL entry
        if entry['severity'] == 'CRITICAL':
            # Add this entry to our critical_events list
            critical_events.append(entry)
    
    # Check if we found any critical events
    if critical_events:
        # Loop through each critical event
        for event in critical_events:
            # Print: [timestamp] message
            # Use both time and date to give full context
            print(f"[{event['date']} {event['time']}] {event['message']}")
    else:
        # No critical events found
        print("No critical events found.")
    
    # Print blank line
    print()


def save_report_to_file(log_entries, output_file='health_report.txt'):
    """
    Save analysis report to a text file
    
    Args:
        log_entries (list): List of parsed log entry dictionaries
        output_file (str): Name of output file
    """
    # Try to create and write to file - catch any errors
    try:
        # open() in write mode ('w') creates new file (overwrites if exists)
        with open(output_file, 'w', encoding='utf-8') as file:
            # Write report header
            file.write("=" * 70 + "\n")
            file.write("SYSTEM HEALTH MONITOR - LOG ANALYSIS REPORT\n")
            # Get current timestamp for report
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 70 + "\n\n")
            
            # Write overall statistics section
            severity_counts = count_by_severity(log_entries)
            file.write("OVERALL STATISTICS\n")
            file.write("-" * 70 + "\n")
            file.write(f"Total Log Entries: {len(log_entries)}\n")
            file.write(f"INFO: {severity_counts['INFO']}\n")
            file.write(f"WARNING: {severity_counts['WARNING']}\n")
            file.write(f"ERROR: {severity_counts['ERROR']}\n")
            file.write(f"CRITICAL: {severity_counts['CRITICAL']}\n\n")
            
            # Write top errors section
            file.write("TOP 5 MOST FREQUENT ERRORS\n")
            file.write("-" * 70 + "\n")
            error_messages = get_error_messages(log_entries)
            top_errors = find_most_frequent_errors(error_messages, top_n=5)
            
            # Loop through top errors and write them
            for index, (message, count) in enumerate(top_errors, start=1):
                file.write(f"{index}. {message} (occurred {count} times)\n")
            
            file.write("\n")
            
            # Write critical events section
            file.write("CRITICAL EVENTS\n")
            file.write("-" * 70 + "\n")
            
            # Get all critical events
            critical_events = [e for e in log_entries if e['severity'] == 'CRITICAL']
            
            # Write each critical event
            for event in critical_events:
                file.write(f"[{event['timestamp']}] {event['message']}\n")
        
        # Print success message
        print(f"✓ Report saved to: {output_file}\n")
        
    # Catch errors during file writing
    except Exception as e:
        # Print error message
        print(f"✗ Error writing report file: {e}\n")


def main():
    """
    Main function to execute log analysis
    This orchestrates all the analysis steps
    """
    # Print welcome banner
    print("\n" + "=" * 70)
    print("SYSTEM HEALTH MONITOR - LOG FILE PARSER")
    print("=" * 70 + "\n")
    
    # Define log file to analyze
    # Change this to analyze different log files
    log_file = 'system.log'
    
    # Print status message
    print(f"Analyzing log file: {log_file}")
    print("Please wait...\n")
    
    # Read and parse the log file
    # This returns a list of dictionaries, or None if error occurred
    log_entries = read_log_file(log_file)
    
    # Check if reading was successful
    if log_entries is None:
        # Reading failed - print error and exit
        print("Failed to read log file. Exiting.")
        return
    
    # Check if we got any valid log entries
    if len(log_entries) == 0:
        # No entries found - print message and exit
        print("No valid log entries found in file.")
        return
    
    # Generate and display the summary report
    generate_summary_report(log_entries)
    
    # Save report to file
    save_report_to_file(log_entries)
    
    # Print completion message
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70 + "\n")


# Entry point - run when script is executed directly
# __name__ == "__main__" is only True when running this file directly
if __name__ == "__main__":
    # Call main function to start the analysis
    main()
