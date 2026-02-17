# User Account Provisioning Automation Script

## Project Overview
A Python automation script that processes bulk user account creation from CSV files. The script validates email addresses, generates standardized usernames, handles errors gracefully, and produces separate output files for successfully processed users and users with validation errors. All actions are logged with timestamps for audit trail purposes.

## Author
**Durgavaraprasad S**  
Date: February 2026

## Purpose
This project demonstrates practical automation skills that directly translate to real-world IT operations. It mirrors the type of PowerShell automation I created in my IT support role, now implemented in Python to showcase programming versatility.

## Skills Demonstrated
- **CSV File Operations**: Reading and writing CSV files
- **Email Validation**: Using regular expressions (regex) for pattern matching
- **Input Validation**: Comprehensive data validation with error handling
- **String Manipulation**: Username generation and text formatting
- **Error Handling**: Try/except blocks for robust error management
- **Logging**: Timestamped action logging for audit trails
- **File I/O**: Reading input files and creating multiple output files
- **Functions**: Modular, reusable code with clear responsibilities
- **Professional Documentation**: Extensive comments and docstrings

## Features
✅ **Email Validation** - Uses regex to verify email format (username@domain.extension)  
✅ **Username Generation** - Creates standardized usernames (first_initial + last_name)  
✅ **Required Field Validation** - Ensures all mandatory fields are present  
✅ **Error Handling** - Gracefully handles missing files, invalid data, and I/O errors  
✅ **Dual Output Files** - Separates successful and failed records  
✅ **Audit Logging** - Timestamps all actions in a log file  
✅ **Statistics Reporting** - Displays processing summary with success rate  

## Technologies Used
- **Python 3.x**
- **csv module** - CSV file reading and writing
- **re module** - Regular expressions for email validation
- **datetime module** - Timestamp generation
- **os module** - File system operations

## Installation & Setup

### Prerequisites
```bash
# Python 3.x required (no additional packages needed - uses standard library)
# Download from: https://www.python.org/downloads/
```

### Running the Project
```bash
# Navigate to project directory
cd /path/to/project

# Run the script
python user_provisioning.py
```

## Input Data Format
The script expects a CSV file named `new_users.csv` with these columns:
- `first_name` - User's first name (required)
- `last_name` - User's last name (required)
- `email` - Email address (required, must be valid format)
- `department` - Department name (required)
- `role` - Job role/title (required)

### Sample Input
```csv
first_name,last_name,email,department,role
John,Smith,john.smith@company.com,IT,System Administrator
Sarah,Johnson,sarah.j@company.com,HR,HR Manager
```

## Output Files

### 1. processed_users.csv
Contains successfully processed users with generated usernames:
```csv
first_name,last_name,email,department,role,username,status
John,Smith,john.smith@company.com,IT,System Administrator,jsmith,Processed
```

### 2. error_users.csv
Contains users who failed validation with error reasons:
```csv
first_name,last_name,email,department,role,status,error_reason
Emily,Brown,,Marketing,Coordinator,Error,Missing required field: email
```

### 3. provisioning.log
Timestamped log of all actions:
```
[2026-02-17 14:30:45] === User Provisioning Started ===
[2026-02-17 14:30:45] Processing users from: new_users.csv
[2026-02-17 14:30:45] Successfully processed: 21 users
[2026-02-17 14:30:45] Errors encountered: 4 users
[2026-02-17 14:30:45] === User Provisioning Completed ===
```

## Sample Output

```
======================================================================
USER ACCOUNT PROVISIONING AUTOMATION
======================================================================

Processing users from: new_users.csv
✓ Output written to: processed_users.csv
✓ Output written to: error_users.csv

======================================================================
PROCESSING SUMMARY
======================================================================
Total Users Processed:     25
Successfully Processed:    21
Errors Encountered:        4
Success Rate:              84.0%
======================================================================

✓ Processing complete!
✓ Log file saved to: provisioning.log
```

## Validation Rules

### Email Validation
- Must contain exactly one @ symbol
- Must have text before @
- Must have domain name after @
- Must have valid extension (.com, .org, etc.)
- Rejects: `jessica.garcia@` (missing domain)
- Rejects: `charles@company` (missing extension)
- Accepts: `john.smith@company.com` ✓

### Username Generation
- Format: first_initial + full_last_name
- All lowercase
- Examples:
  - John Smith → `jsmith`
  - Sarah Johnson → `sjohnson`
  - Michael Williams → `mwilliams`

### Required Fields
All five fields must have values:
1. first_name
2. last_name
3. email
4. department
5. role

## Real-World Applications
This script can be used for:
1. **Bulk User Creation** - Onboard multiple new employees at once
2. **Active Directory Pre-Processing** - Validate data before AD import
3. **HR System Integration** - Process employee data exports
4. **Audit Compliance** - Timestamped logs for compliance requirements
5. **Error Prevention** - Catch data issues before they reach production systems

## Project Impact
- **Reduces manual data entry by 100%** - Automates what would be hours of manual work
- **Eliminates typos** - Standardized username generation prevents inconsistencies
- **Catches errors early** - Validates data before it reaches production systems
- **Provides audit trail** - Log file documents all processing for compliance
- **Scales infinitely** - Can process 10 or 10,000 users in seconds

## Connection to My Background
This project directly applies my 6+ years of IT operations experience:

**From My Resume:**
- *"Provisioning 200+ user accounts"* → This automates that exact process
- *"Office 365 environment management"* → Username generation follows O365 standards
- *"Created 10+ PowerShell scripts"* → This is the Python equivalent of my PowerShell automation
- *"Reduced manual effort by 40%"* → This script reduces effort by 100%

**Real Scenarios I've Encountered:**
- Bulk onboarding of new hires during company acquisitions
- Migrating users between systems with standardized naming
- Validating HR data exports before AD import
- Generating audit logs for compliance reviews

## Error Handling Examples

### Missing Email
```
Input:  Emily,Brown,,Marketing,Marketing Coordinator
Output: Missing required field: email
```

### Invalid Email Format
```
Input:  Jessica,Garcia,jessica.garcia@,Sales,Representative
Output: Invalid email format: jessica.garcia@
```

### Missing Name
```
Input:  ,Thompson,chris.thompson@company.com,Finance,Accountant
Output: Missing required field: first_name
```

## Future Enhancements
- [ ] Add duplicate username detection and resolution
- [ ] Generate random secure passwords
- [ ] Send welcome emails with credentials
- [ ] Integration with Active Directory (python-ldap)
- [ ] Excel file support (openpyxl)
- [ ] Department-based username prefixes
- [ ] Batch size limiting for large files
- [ ] GUI interface using tkinter

## Key Learnings
Through this project, I strengthened my understanding of:
- Regular expressions for pattern matching
- CSV file manipulation in Python
- Error handling best practices
- Logging and audit trail creation
- Modular function design
- Input validation techniques
- File I/O operations

## Code Quality
- **Lines of Code:** ~350 lines (including extensive comments)
- **Functions:** 7 well-defined functions with single responsibilities
- **Comment Density:** ~45% of code is educational comments
- **Error Handling:** Comprehensive try/except blocks throughout
- **Readability:** Every complex operation explained line-by-line

## Testing the Script

### Create Test Input File
```csv
first_name,last_name,email,department,role
Test,User1,test1@company.com,IT,Tester
Test,User2,invalid-email,IT,Tester
Test,User3,test3@company.com,IT,Tester
```

### Expected Results
- User1 and User3: Successfully processed
- User2: Error (invalid email format)
- Success rate: 66.7%

## License
This project is available for educational and portfolio purposes.

## Contact
**Durgavaraprasad S**  
📧 durgavaraprasad09@gmail.com  
🔗 [linkedin.com/in/dvps](https://linkedin.com/in/dvps)  
📍 Tirupati, Andhra Pradesh, India

---
*This project demonstrates the practical application of Python programming to automate real-world IT operations tasks.*
