# Placement Eligibility and Skill-Gap Analyzer

## 1. Project Overview

The **Placement Eligibility and Skill-Gap Analyzer** is a Python-based application that evaluates student profiles against job requirements.

It reads student information and job criteria from CSV files, checks placement eligibility, calculates skill-match percentages, identifies missing skills, and generates an eligibility report.

The main objective is to help students understand their eligibility for different job opportunities and identify the skills they may need to improve.

## 2. Features

- Reads student profiles from a CSV file.
- Reads job requirements from a separate CSV file.
- Validates input records and required columns.
- Normalizes skills for accurate comparison.
- Calculates skill-match percentages.
- Checks programme and minimum CGPA requirements.
- Identifies matched and missing skills.
- Generates an eligibility report in CSV format.
- Handles invalid data and missing files.
- Demonstrates recursion using nested skill categories.
- Includes automated unit tests.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| CSV module | Reading and writing CSV files |
| Unittest | Automated testing |
| Math module | Numeric validation |
| Git and GitHub | Version control and project hosting |

## 4. Project Structure

```text
Placement_Eligibility_Analyzer/
│
├── main.py
├── students.csv
├── jobs.csv
├── eligibility_report.csv
├── test_main.py
├── claim_verification.md
├── scoring_formula.md
├── AI_Verification_Log.md
└── README.md
```

## 5. Input Files

### students.csv

Contains student information.

| Column | Description |
|---|---|
| student_id | Unique student identifier |
| name | Student name |
| programme | Academic programme |
| cgpa | Student CGPA |
| skills | Semicolon-separated skills |

Example:

```csv
student_id,name,programme,cgpa,skills
101,Rahul,MCA,8.5,Python;SQL;FastAPI
102,Priya,MCA,7.8,Python;SQL
```

### jobs.csv

Contains job requirements.

| Column | Description |
|---|---|
| job_id | Unique job identifier |
| company | Company name |
| role | Job role |
| programme | Required academic programme |
| min_cgpa | Minimum required CGPA |
| required_skills | Semicolon-separated required skills |

Example:

```csv
job_id,company,role,programme,min_cgpa,required_skills
J101,TCS,Python Developer,MCA,7.0,Python;SQL;FastAPI
J102,Infosys,Web Developer,BCA,6.5,HTML;CSS;JavaScript
```

## 6. Skill-Match Scoring Formula

The application uses the following formula:

**Skill Match Score = (Matched Skills / Total Required Skills) × 100**

For example, if a student has two out of three required skills:

**Score = (2 / 3) × 100 = 66.67%**

The score represents skill overlap, not actual technical proficiency.

For the complete explanation, refer to `scoring_formula.md`.

## 7. Eligibility Criteria

A student is marked eligible only if all three conditions are satisfied:

1. The student's programme matches the job requirement.
2. The student's CGPA meets or exceeds the minimum CGPA.
3. All required job skills are present in the student's profile.

If any condition fails, the student is marked as not eligible.

## 8. Installation and Execution

### Prerequisites

- Python 3 installed on your computer.
- A terminal or command prompt.

No external Python packages are required for the core application.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace the placeholder with the actual repository URL.

### Step 2: Open the Project Folder

```bash
cd Placement_Eligibility_Analyzer
```

### Step 3: Run the Application

```bash
python3 main.py
```

The application reads the input CSV files, evaluates student eligibility, displays the results, and generates the report.

## 9. Running Automated Tests

The project includes unit tests for important functions and validation scenarios.

Run the test suite using:

```bash
python3 -m unittest test_main -v
```

**Development test result:** All 18 tests passed during the recorded test run.

The tests cover:

- Skill normalization.
- Skill matching.
- Missing skills.
- Programme mismatch.
- CGPA validation.
- Duplicate student IDs.
- Missing CSV files and columns.
- Invalid numeric values.
- Report generation.
- Recursive function behaviour.

## 10. Output File

### eligibility_report.csv

The application generates an eligibility report containing the student and job comparison results.

The report includes:

- Student information.
- Company and job role.
- Skill-match percentage.
- Matched skills.
- Missing skills.
- Eligibility status.
- Reasons for ineligibility.

The generated report can be opened using spreadsheet applications such as Microsoft Excel or Google Sheets.

## 11. Error Handling and Validation

The application includes validation for:

- Missing input files.
- Missing required CSV columns.
- Missing or invalid student information.
- Invalid CGPA values.
- CGPA values outside the accepted range.
- Duplicate student IDs.
- Malformed CSV records.

These checks help prevent incorrect or incomplete records from being processed.

## 12. Recursive Function

The project demonstrates recursion through a function that displays nested skill categories.

It includes demonstrations of:

- Empty input.
- A single nested child.
- Multiple nested levels.

The recursion examples help demonstrate how a function can call itself to process nested structures.

## 13. Ethical Considerations and Limitations

- The system uses only the information provided in the input files.
- It does not infer skills from student names, colleges, or personal backgrounds.
- Skill-match scores do not represent verified technical proficiency.
- Eligibility results depend on the accuracy of the supplied information.
- The application is a decision-support tool, not a replacement for human recruitment decisions.

## 14. Additional Documentation

The following files provide further details:

| File | Purpose |
|---|---|
| `scoring_formula.md` | Scoring formula and eligibility logic |
| `claim_verification.md` | Verification of technical claims |
| `AI_Verification_Log.md` | Record of AI assistance and verification |
| `test_main.py` | Automated test cases |

## 15. Conclusion

The Placement Eligibility and Skill-Gap Analyzer demonstrates the practical application of Python programming, CSV processing, data validation, conditional statements, loops, recursion, and automated testing.

It provides a transparent way to compare student profiles with job requirements and identify potential skill gaps.

---

**Project:** Placement Eligibility and Skill-Gap Analyzer
**Language:** Python
**Project Type:** Academic Case Study
