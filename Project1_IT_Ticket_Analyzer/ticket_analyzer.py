"""
IT Ticket Analyzer & Report Generator
Author: Durgavaraprasad S
Date: February 2026

Purpose: Analyze IT support tickets from CSV file and generate comprehensive reports
on ticket trends, resolution times, and category distributions.

Skills Demonstrated:
- CSV file handling and data import
- Pandas DataFrame operations (filtering, grouping, aggregating)
- Data analysis and statistical calculations
- Report generation and formatted output
- Error handling and validation
"""

# Import the pandas library for data manipulation and analysis
# Pandas is like Excel for Python - it lets us work with tables of data
import pandas as pd

# Import sys module for system operations like exiting the program
import sys

# Import datetime to get current date/time for report timestamps
from datetime import datetime

def load_ticket_data(filename):
    """
    Load IT ticket data from CSV file
    
    Args:
        filename (str): Path to the CSV file containing ticket data
        
    Returns:
        pandas.DataFrame: DataFrame containing ticket data, or None if error occurs
    """
    # Try to load the file - if anything goes wrong, we'll catch the error
    try:
        # Read the CSV file and convert it into a DataFrame (like a spreadsheet in Python)
        # pd.read_csv() automatically reads the first row as column headers
        df = pd.read_csv(filename)
        
        # len(df) counts how many rows (tickets) are in the DataFrame
        # Print success message with the number of tickets loaded
        print(f"✓ Successfully loaded {len(df)} tickets from {filename}\n")
        
        # Return the DataFrame so other functions can use it
        return df
        
    # If the file doesn't exist, this error will trigger
    except FileNotFoundError:
        # Print an error message telling the user the file wasn't found
        print(f"✗ Error: File '{filename}' not found.")
        # Return None to indicate failure
        return None
        
    # Catch any other unexpected errors that might occur
    except Exception as e:
        # 'e' contains the error message - print it so we know what went wrong
        print(f"✗ Error loading file: {e}")
        # Return None to indicate failure
        return None


def validate_data(df):
    """
    Validate that the DataFrame has required columns
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Create a list of column names that must exist in our CSV file
    # Without these columns, we can't do our analysis
    required_columns = ['ticket_id', 'priority', 'status', 'resolution_time_hours', 'category']
    
    # Check if all required columns exist in the DataFrame
    # List comprehension: loop through each required column and check if it's NOT in df.columns
    # If a column is missing, it gets added to the missing_columns list
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    # If missing_columns list has any items in it, validation failed
    if missing_columns:
        # Join all missing column names with commas and print error message
        print(f"✗ Error: Missing required columns: {', '.join(missing_columns)}")
        # Return False to indicate validation failed
        return False
    
    # If we get here, all required columns exist - print success message
    print("✓ Data validation passed\n")
    # Return True to indicate validation passed
    return True


def analyze_by_priority(df):
    """
    Analyze tickets grouped by priority level
    
    Args:
        df (pandas.DataFrame): DataFrame containing ticket data
        
    Returns:
        pandas.DataFrame: Summary statistics by priority
    """
    # Print a separator line (70 equals signs) to make output readable
    print("=" * 70)
    # Print the section header
    print("ANALYSIS BY PRIORITY")
    # Print another separator line
    print("=" * 70)
    
    # Group tickets by their priority level and calculate statistics
    # .groupby('priority') - Groups all tickets with same priority together (like GROUP BY in SQL)
    # .agg() - Aggregation function, lets us calculate multiple statistics at once
    priority_stats = df.groupby('priority').agg({
        # For 'ticket_id' column: count how many tickets exist (each ticket has unique ID)
        'ticket_id': 'count',  # Count number of tickets
        
        # For 'resolution_time_hours' column: calculate mean, min, and max
        # This gives us average, fastest, and slowest resolution times
        'resolution_time_hours': ['mean', 'min', 'max']  # Calculate avg, min, max resolution time
    }).round(2)  # Round all numbers to 2 decimal places for readability
    
    # The column names from .agg() are multi-level and confusing
    # Rename them to be clear and user-friendly
    priority_stats.columns = ['Total Tickets', 'Avg Resolution (hrs)', 'Min Resolution (hrs)', 'Max Resolution (hrs)']
    
    # Sort the results by priority level (we want Critical first, then High, Medium, Low)
    # Create a list defining the order we want
    priority_order = ['Critical', 'High', 'Medium', 'Low']
    # .reindex() reorders the rows according to our priority_order list
    priority_stats = priority_stats.reindex(priority_order)
    
    # Print the formatted table to the console
    print(priority_stats)
    # Print a blank line for spacing
    print()
    
    # Return the statistics so other functions can use them if needed
    return priority_stats


def analyze_by_category(df):
    """
    Analyze tickets grouped by category
    
    Args:
        df (pandas.DataFrame): DataFrame containing ticket data
        
    Returns:
        pandas.DataFrame: Summary statistics by category
    """
    # Print separator lines and header for this analysis section
    print("=" * 70)
    print("ANALYSIS BY CATEGORY")
    print("=" * 70)
    
    # Group all tickets by their category (Network, Software, Hardware, etc.)
    # .groupby('category') - Groups tickets with the same category together
    # .agg() - Calculate statistics for each group
    category_stats = df.groupby('category').agg({
        # Count how many tickets exist in each category
        'ticket_id': 'count',
        # Calculate the average resolution time for each category
        'resolution_time_hours': 'mean'
    }).round(2)  # Round numbers to 2 decimal places
    
    # Rename the columns to be more descriptive
    category_stats.columns = ['Total Tickets', 'Avg Resolution (hrs)']
    
    # Sort the categories by total ticket count in descending order
    # ascending=False means highest numbers first (most common categories at top)
    category_stats = category_stats.sort_values('Total Tickets', ascending=False)
    
    # Print the formatted table
    print(category_stats)
    # Print blank line for spacing
    print()
    
    # Return the statistics DataFrame
    return category_stats


def calculate_overall_metrics(df):
    """
    Calculate overall ticket metrics
    
    Args:
        df (pandas.DataFrame): DataFrame containing ticket data
        
    Returns:
        dict: Dictionary containing overall metrics
    """
    # Print section header
    print("=" * 70)
    print("OVERALL METRICS")
    print("=" * 70)
    
    # Create a dictionary to store all our calculated metrics
    # Dictionaries store key-value pairs, like: 'total_tickets': 100
    metrics = {
        # len(df) counts total number of rows (tickets) in the DataFrame
        'total_tickets': len(df),
        
        # .mean() calculates the average of all values in the 'resolution_time_hours' column
        'avg_resolution_time': df['resolution_time_hours'].mean(),
        
        # .median() finds the middle value (50th percentile) - useful when there are outliers
        'median_resolution_time': df['resolution_time_hours'].median(),
        
        # .min() finds the smallest resolution time (fastest ticket resolved)
        'min_resolution_time': df['resolution_time_hours'].min(),
        
        # .max() finds the largest resolution time (slowest ticket resolved)
        'max_resolution_time': df['resolution_time_hours'].max(),
        
        # df[df['priority'] == 'Critical'] filters to only show Critical priority tickets
        # len() then counts how many Critical tickets exist
        'critical_tickets': len(df[df['priority'] == 'Critical']),
        
        # Same logic: filter for High priority, then count them
        'high_tickets': len(df[df['priority'] == 'High']),
        
        # Filter for Resolved status tickets and count them
        'resolved_tickets': len(df[df['status'] == 'Resolved'])
    }
    
    # Now print all the metrics in a formatted, easy-to-read way
    # metrics['key'] accesses the value stored under that key in our dictionary
    
    # Print total tickets analyzed
    print(f"Total Tickets Analyzed:        {metrics['total_tickets']}")
    
    # Print resolved tickets count and calculate percentage
    # (resolved / total * 100) gives us the percentage, :.1f formats to 1 decimal place
    print(f"Resolved Tickets:              {metrics['resolved_tickets']} ({(metrics['resolved_tickets']/metrics['total_tickets']*100):.1f}%)")
    
    # Print critical tickets count and percentage
    print(f"Critical Priority Tickets:     {metrics['critical_tickets']} ({(metrics['critical_tickets']/metrics['total_tickets']*100):.1f}%)")
    
    # Print high priority tickets count and percentage
    print(f"High Priority Tickets:         {metrics['high_tickets']} ({(metrics['high_tickets']/metrics['total_tickets']*100):.1f}%)")
    
    # Print a blank line to separate sections
    print(f"\nAverage Resolution Time:       {metrics['avg_resolution_time']:.2f} hours")
    
    # :.2f means format the number with 2 decimal places
    print(f"Median Resolution Time:        {metrics['median_resolution_time']:.2f} hours")
    print(f"Fastest Resolution:            {metrics['min_resolution_time']:.2f} hours")
    print(f"Slowest Resolution:            {metrics['max_resolution_time']:.2f} hours")
    
    # Print blank line for spacing
    print()
    
    # Return the metrics dictionary so other functions can use these calculations
    return metrics


def identify_trends(df):
    """
    Identify key trends and insights from ticket data
    
    Args:
        df (pandas.DataFrame): DataFrame containing ticket data
    """
    # Print section header
    print("=" * 70)
    print("KEY INSIGHTS & TRENDS")
    print("=" * 70)
    
    # Find the most common issue category
    # .value_counts() counts how many times each category appears
    # .index[0] gets the name of the category with the highest count (first item)
    top_category = df['category'].value_counts().index[0]
    
    # .values[0] gets the actual count number for the most common category
    top_category_count = df['category'].value_counts().values[0]
    
    # Print the most common category and how many tickets it had
    print(f"• Most Common Issue Type:      {top_category} ({top_category_count} tickets)")
    
    # Find which category takes longest to resolve on average
    # .groupby('category') groups tickets by category
    # ['resolution_time_hours'].mean() calculates average resolution time for each category
    # .idxmax() returns the category name (index) with the maximum average time
    slowest_category = df.groupby('category')['resolution_time_hours'].mean().idxmax()
    
    # Get the actual average time value for the slowest category
    slowest_avg_time = df.groupby('category')['resolution_time_hours'].mean().max()
    
    print(f"• Slowest Category to Resolve: {slowest_category} (avg {slowest_avg_time:.2f} hrs)")
    
    # Find which category resolves fastest on average
    # .idxmin() returns the category name with the minimum average time
    fastest_category = df.groupby('category')['resolution_time_hours'].mean().idxmin()
    
    # Get the actual average time value for the fastest category
    fastest_avg_time = df.groupby('category')['resolution_time_hours'].mean().min()
    
    print(f"• Fastest Category to Resolve: {fastest_category} (avg {fastest_avg_time:.2f} hrs)")
    
    # Calculate average resolution time for Critical priority tickets only
    # df[df['priority'] == 'Critical'] filters to only Critical tickets
    # ['resolution_time_hours'].mean() calculates their average resolution time
    critical_avg = df[df['priority'] == 'Critical']['resolution_time_hours'].mean()
    print(f"• Critical Ticket Avg Response: {critical_avg:.2f} hours")
    
    # Count how many tickets were resolved in under 2 hours
    # df['resolution_time_hours'] < 2 creates a True/False for each ticket
    # len() counts how many True values (tickets under 2 hours)
    quick_tickets = len(df[df['resolution_time_hours'] < 2])
    
    # Calculate what percentage of total tickets were resolved quickly
    quick_percentage = (quick_tickets / len(df)) * 100
    
    print(f"• Tickets Resolved Under 2hrs: {quick_tickets} ({quick_percentage:.1f}%)")
    
    # Print blank line for spacing
    print()


def generate_report_file(df, filename='ticket_analysis_report.txt'):
    """
    Generate a text file report with all analysis results
    
    Args:
        df (pandas.DataFrame): DataFrame containing ticket data
        filename (str): Output filename for the report
    """
    # Try to create and write to the file - catch any errors that might occur
    try:
        # open() opens a file for writing ('w' mode means write, will overwrite if exists)
        # 'with' ensures the file closes properly even if an error occurs
        # 'f' is the variable name we'll use to refer to the open file
        with open(filename, 'w') as f:
            
            # Write header section to the file
            # f.write() writes a string to the file (\n means new line)
            f.write("=" * 70 + "\n")
            f.write("IT TICKET ANALYSIS REPORT\n")
            
            # Get current date and time, format it nicely (YYYY-MM-DD HH:MM:SS)
            # datetime.now() gets the current moment
            # .strftime() formats it as a string
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")
            
            # Calculate overall metrics by calling our function
            # This returns a dictionary with all the statistics
            metrics = calculate_overall_metrics(df)
            
            # Write overall metrics section
            f.write("OVERALL METRICS\n")
            f.write("-" * 70 + "\n")
            
            # Access values from the metrics dictionary and write them to file
            f.write(f"Total Tickets: {metrics['total_tickets']}\n")
            f.write(f"Average Resolution Time: {metrics['avg_resolution_time']:.2f} hours\n")
            f.write(f"Critical Tickets: {metrics['critical_tickets']}\n\n")
            
            # Write priority breakdown section
            f.write("TICKETS BY PRIORITY\n")
            f.write("-" * 70 + "\n")
            
            # .value_counts() counts how many tickets exist for each priority level
            # Returns a Series with priority names and their counts
            priority_counts = df['priority'].value_counts()
            
            # Loop through each priority and its count
            # .items() gives us both the priority name and the count
            for priority, count in priority_counts.items():
                # Write each priority and its count to the file
                f.write(f"{priority}: {count} tickets\n")
            
            # Write a blank line for spacing
            f.write("\n")
            
            # Write category breakdown section
            f.write("TICKETS BY CATEGORY\n")
            f.write("-" * 70 + "\n")
            
            # Count tickets in each category
            category_counts = df['category'].value_counts()
            
            # Loop through and write each category and its count
            for category, count in category_counts.items():
                f.write(f"{category}: {count} tickets\n")
        
        # If we get here, file was written successfully
        # Print success message with the filename
        print(f"✓ Report saved to: {filename}\n")
        
    # Catch any errors that might occur during file writing
    except Exception as e:
        # Print error message with the specific error details
        print(f"✗ Error generating report file: {e}\n")


def main():
    """
    Main function to execute the ticket analysis
    This is the "orchestrator" - it calls all our other functions in the right order
    """
    # Print welcome banner with nice formatting
    print("\n" + "=" * 70)
    print("IT TICKET ANALYZER & REPORT GENERATOR")
    print("=" * 70 + "\n")
    
    # Define which CSV file to analyze
    # You can change this to analyze different files
    csv_file = 'it_tickets.csv'
    
    # Call the load_ticket_data function to read the CSV file
    # Store the result (DataFrame) in the variable 'df'
    df = load_ticket_data(csv_file)
    
    # Check if df is None (which means loading failed)
    if df is None:
        # Print error message
        print("Exiting due to data loading error.")
        # sys.exit(1) stops the program immediately
        # The '1' indicates an error occurred (0 would mean success)
        sys.exit(1)
    
    # Validate that the DataFrame has all required columns
    # validate_data returns True or False
    if not validate_data(df):
        # If validation failed (returned False), print error and exit
        print("Exiting due to data validation error.")
        sys.exit(1)
    
    # If we get here, data loaded and validated successfully!
    # Now perform all our analyses by calling each function
    
    # Calculate and display overall metrics
    calculate_overall_metrics(df)
    
    # Analyze tickets grouped by priority level
    analyze_by_priority(df)
    
    # Analyze tickets grouped by category
    analyze_by_category(df)
    
    # Identify trends and key insights
    identify_trends(df)
    
    # Generate a text file report with all results
    generate_report_file(df)
    
    # Print completion message
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70 + "\n")


# This is the entry point of the program
# __name__ == "__main__" is True only when you run this file directly
# (not when you import it as a module in another file)
if __name__ == "__main__":
    # Call the main function to start the analysis
    main()
