
import csv
import math


# ==========================================
# 1. READ AND VALIDATE CSV FILES
# ==========================================

def read_csv_file(filename, required_columns):

    data = []

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(
                file,
                restkey="extra_fields",
                restval=None
            )

            if not reader.fieldnames:
                print(f"Error: {filename} is empty.")
                return []

            # Normalize column headings
            reader.fieldnames = [
                name.strip() if name else ""
                for name in reader.fieldnames
            ]

            # Check duplicate column names
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                print(f"Error: Duplicate column names in {filename}.")
                return []

            # Check required columns
            missing_columns = (
                set(required_columns) - set(reader.fieldnames)
            )

            if missing_columns:
                print(
                    f"Error: Missing columns in {filename}: "
                    f"{', '.join(sorted(missing_columns))}"
                )
                return []

            # Read individual records
            for row_number, row in enumerate(reader, start=2):

                # Detect extra values
                if row.get("extra_fields") is not None:
                    print(
                        f"Warning: Extra values in row {row_number}."
                    )
                    continue

                # Check missing values
                if any(
                    row.get(column) is None
                    or not str(row[column]).strip()
                    for column in required_columns
                ):
                    print(
                        f"Warning: Missing values in row {row_number}."
                    )
                    continue

                # Remove unnecessary spaces
                for key in row:
                    if isinstance(row[key], str):
                        row[key] = row[key].strip()

                data.append(row)

    except FileNotFoundError:
        print(f"Error: {filename} not found.")

    except (OSError, csv.Error, UnicodeError) as error:
        print(f"Error reading {filename}: {error}")

    return data


# ==========================================
# 2. NORMALIZE SKILLS
# ==========================================

def normalize_skills(skill_text):

    if not isinstance(skill_text, str):
        return set()

    return {
        skill.strip().lower()
        for skill in skill_text.split(";")
        if skill.strip()
    }


# ==========================================
# 3. VALIDATE STUDENT AND JOB RECORDS
# ==========================================

def validate_records(records, record_type):

    valid_records = []
    seen_ids = set()

    if record_type == "student":

        id_column = "student_id"
        numeric_column = "cgpa"

        required_fields = [
            "student_id",
            "name",
            "programme",
            "skills"
        ]

    elif record_type == "job":

        id_column = "job_id"
        numeric_column = "min_cgpa"

        required_fields = [
            "job_id",
            "company",
            "role",
            "programme",
            "required_skills"
        ]

    else:
        raise ValueError("Invalid record type.")

    for row_number, record in enumerate(records, start=2):

        if not isinstance(record, dict):
            print(
                f"Invalid {record_type} row {row_number}: "
                "Invalid record format."
            )
            continue

        record_id = record.get(id_column)

        if not isinstance(record_id, str):
            print(
                f"Invalid {record_type} row {row_number}: "
                "Missing record ID."
            )
            continue

        record_id = record_id.strip()

        if not record_id:
            print(
                f"Invalid {record_type} row {row_number}: "
                "Missing record ID."
            )
            continue

        # Check duplicate IDs
        if record_id.lower() in seen_ids:
            print(
                f"Invalid {record_type} row {row_number}: "
                "Duplicate ID."
            )
            continue

        # Check required text fields
        if any(
            not isinstance(record.get(field), str)
            or not record[field].strip()
            for field in required_fields
        ):
            print(
                f"Invalid {record_type} row {row_number}: "
                "Missing required information."
            )
            continue

        # Validate CGPA
        try:
            value = float(record[numeric_column])

            if not math.isfinite(value) or not 0 <= value <= 10:
                print(
                    f"Invalid {record_type} row {row_number}: "
                    "CGPA must be between 0 and 10."
                )
                continue

        except (ValueError, TypeError):
            print(
                f"Invalid {record_type} row {row_number}: "
                "Invalid CGPA value."
            )
            continue

        # Check that skill information is present
        skill_field = (
            "skills" if record_type == "student"
            else "required_skills"
        )

        if not normalize_skills(record[skill_field]):
            print(
                f"Invalid {record_type} row {row_number}: "
                "At least one skill is required."
            )
            continue

        seen_ids.add(record_id.lower())
        valid_records.append(record)

    return valid_records


# ==========================================
# 4. CHECK STUDENT ELIGIBILITY
# ==========================================

def check_eligibility(student, job):

    student_skills = normalize_skills(
        student["skills"]
    )

    required_skills = normalize_skills(
        job["required_skills"]
    )

    # Compare student and job skills
    matched = student_skills & required_skills

    missing = required_skills - student_skills

    # Calculate skill-match percentage
    if required_skills:

        score = (
            len(matched) / len(required_skills)
        ) * 100

    else:
        score = 0.0

    reasons = []

    # Check programme
    if (
        student["programme"].strip().lower()
        != job["programme"].strip().lower()
    ):
        reasons.append("Programme does not match")

    # Check CGPA
    try:

        student_cgpa = float(student["cgpa"])
        minimum_cgpa = float(job["min_cgpa"])

        if (
            not math.isfinite(student_cgpa)
            or not 0 <= student_cgpa <= 10
        ):
            reasons.append("Invalid student CGPA")

        elif (
            not math.isfinite(minimum_cgpa)
            or not 0 <= minimum_cgpa <= 10
        ):
            reasons.append("Invalid job minimum CGPA")

        elif student_cgpa < minimum_cgpa:
            reasons.append(
                "CGPA below minimum requirement"
            )

    except (ValueError, TypeError):
        reasons.append("Invalid CGPA value")

    # Check missing skills
    if missing:
        reasons.append(
            "Missing required skills: "
            + ", ".join(sorted(missing))
        )

    eligible = len(reasons) == 0

    return {
        "eligible": eligible,
        "score": round(score, 2),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "reasons": reasons
    }


# ==========================================
# 5. DISPLAY STUDENT DETAILS
# ==========================================

def display_students(students):

    print("\n========== STUDENT DETAILS ==========")

    for student in students:

        print("ID:", student["student_id"])
        print("Name:", student["name"])
        print("Programme:", student["programme"])
        print("CGPA:", student["cgpa"])
        print("Skills:", student["skills"])
        print("--------------------------------")


# ==========================================
# 6. DISPLAY JOB REQUIREMENTS
# ==========================================

def display_jobs(jobs):

    print("\n========== JOB REQUIREMENTS ==========")

    for job in jobs:

        print("Job ID:", job["job_id"])
        print("Company:", job["company"])
        print("Role:", job["role"])
        print("Programme:", job["programme"])
        print("Minimum CGPA:", job["min_cgpa"])
        print("Required Skills:", job["required_skills"])
        print("--------------------------------")


# ==========================================
# 7. COMPARE EVERY STUDENT WITH EVERY JOB
# ==========================================

def display_results(students, jobs):

    print(
        "\n========== PLACEMENT ELIGIBILITY RESULTS =========="
    )

    for student in students:

        for job in jobs:

            result = check_eligibility(student, job)

            print("\nStudent:", student["name"])
            print("Company:", job["company"])
            print("Role:", job["role"])

            print(
                "Skill Match:",
                str(result["score"]) + "%"
            )

            print(
                "Matched Skills:",
                ", ".join(result["matched"]) or "None"
            )

            print(
                "Missing Skills:",
                ", ".join(result["missing"]) or "None"
            )

            if result["eligible"]:

                print("Status: MEETS CRITERIA")

            else:

                print("Status: DOES NOT MEET CRITERIA")

                print(
                    "Reasons:",
                    "; ".join(result["reasons"])
                )

            print("--------------------------------")


# ==========================================
# 8. GENERATE PLACEMENT ELIGIBILITY REPORT
# ==========================================

def generate_report(students, jobs):

    filename = "eligibility_report.csv"

    columns = [
        "Student ID",
        "Student Name",
        "Company",
        "Job Role",
        "Skill Match (%)",
        "Matched Skills",
        "Missing Skills",
        "Eligibility Status",
        "Unmet Criteria"
    ]

    try:

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=columns
            )

            writer.writeheader()

            for student in students:

                for job in jobs:

                    result = check_eligibility(
                        student,
                        job
                    )

                    writer.writerow({

                        "Student ID":
                            student["student_id"],

                        "Student Name":
                            student["name"],

                        "Company":
                            job["company"],

                        "Job Role":
                            job["role"],

                        "Skill Match (%)":
                            result["score"],

                        "Matched Skills":
                            "; ".join(result["matched"]),

                        "Missing Skills":
                            "; ".join(result["missing"]),

                        "Eligibility Status": (
                            "MEETS CRITERIA"
                            if result["eligible"]
                            else "DOES NOT MEET CRITERIA"
                        ),

                        "Unmet Criteria": (
                            "; ".join(result["reasons"])
                            if result["reasons"]
                            else "None"
                        )
                    })

        print(
            f"\nReport generated successfully: {filename}"
        )

    except OSError as error:

        print("Error generating report:", error)


# ==========================================
# 9. SCORING FORMULA EXPLANATION
# ==========================================

def display_scoring_formula():

    print("\n========== SCORING FORMULA ==========")

    print(
        "Skill Match (%) = "
        "(Matched Skills / Required Skills) * 100"
    )

    print("\nEligibility Conditions:")

    print("1. Student programme must match the job programme.")

    print("2. Student CGPA must meet the minimum CGPA.")

    print("3. All required job skills must be matched.")

    print("\nLimitations:")

    print(
        "- Skill matching uses keywords, not practical skill tests."
    )

    print(
        "- The score does not measure actual technical expertise."
    )

    print(
        "- Only the provided CSV information is considered."
    )

    print(
        "- Names and institutions are not used to infer ability."
    )


# ==========================================
# 10. RECURSIVE FUNCTION FOR NESTED SKILLS
# ==========================================

def display_skills(category, level=0):

    for skill, subskills in category.items():

        print("  " * level + "- " + skill)

        if isinstance(subskills, dict):

            display_skills(
                subskills,
                level + 1
            )


# ==========================================
# 11. EXAMPLE NESTED SKILL CATEGORIES
# ==========================================

skill_categories = {

    "Programming": {

        "Python": {

            "FastAPI": {},

            "Django": {}

        },

        "Java": {}

    },

    "Database": {

        "SQL": {

            "PostgreSQL": {},

            "MySQL": {}

        }

    }

}


# ==========================================
# 12. AUTOMATED RECURSION DEMONSTRATIONS
# ==========================================

def run_recursion_tests():

    print("\n========== RECURSION TESTS ==========")

    test_cases = [

        (
            "Empty category",
            {}
        ),

        (
            "Single child",
            {
                "Programming": {
                    "Python": {}
                }
            }
        ),

        (
            "Multiple children",
            {
                "Programming": {
                    "Python": {},
                    "Java": {},
                    "C++": {}
                }
            }
        ),

        (
            "Multiple nested levels",
            {
                "Programming": {
                    "Python": {
                        "Web Development": {
                            "FastAPI": {},
                            "Django": {}
                        }
                    }
                },
                "Database": {
                    "SQL": {
                        "PostgreSQL": {}
                    }
                }
            }
        )
    ]

    for test_number, (test_name, category) in enumerate(
        test_cases,
        start=1
    ):

        print(f"\nTest {test_number}: {test_name}")

        display_skills(category)

        print("Demonstration completed.")

    print("\nAll recursion demonstrations completed.")


# ==========================================
# 13. MAIN PROGRAM EXECUTION
# ==========================================

def main():

    print("\n========== PLACEMENT ELIGIBILITY ANALYZER ==========")

    # Load student data
    students = read_csv_file(
        "students.csv",
        ["student_id", "name", "programme", "cgpa", "skills"]
    )

    # Load job data
    jobs = read_csv_file(
        "jobs.csv",
        [
            "job_id",
            "company",
            "role",
            "programme",
            "min_cgpa",
            "required_skills"
        ]
    )

    # Validate records
    students = validate_records(students, "student")
    jobs = validate_records(jobs, "job")

    print("\n========== INPUT VALIDATION ==========")
    print("Valid students:", len(students))
    print("Valid jobs:", len(jobs))

    # Display input data
    display_students(students)
    display_jobs(jobs)

    # Display eligibility comparisons
    display_results(students, jobs)

    # Generate CSV report
    generate_report(students, jobs)

    # Display scoring explanation
    display_scoring_formula()

    # Display nested skill categories
    print("\n========== NESTED SKILL CATEGORIES ==========")
    display_skills(skill_categories)

    # Run recursion demonstrations
    run_recursion_tests()

    print(
        "\n========== PROGRAM EXECUTION COMPLETED =========="
    )


# Execute only when this file is run directly
if __name__ == "__main__":

    main()
