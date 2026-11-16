
import csv
import os
import tempfile
import unittest

from main import (
    normalize_skills,
    check_eligibility,
    validate_records,
    read_csv_file,
    generate_report,
    display_skills
)


class TestPlacementEligibilityAnalyzer(unittest.TestCase):

    def setUp(self):

        self.student = {
            "student_id": "101",
            "name": "Rahul",
            "programme": "MCA",
            "cgpa": "8.5",
            "skills": "Python;SQL;FastAPI"
        }

        self.job = {
            "job_id": "J101",
            "company": "TCS",
            "role": "Python Developer",
            "programme": "MCA",
            "min_cgpa": "7.0",
            "required_skills": "Python;SQL;FastAPI"
        }

    # Test 1: Skill normalization
    def test_skill_normalization(self):

        result = normalize_skills(" Python ; SQL ; FastAPI ")

        self.assertEqual(
            result,
            {"python", "sql", "fastapi"}
        )

    # Test 2: All skills matched
    def test_all_skills_matched(self):

        result = check_eligibility(
            self.student,
            self.job
        )

        self.assertEqual(result["score"], 100.0)
        self.assertTrue(result["eligible"])

    # Test 3: Missing skill
    def test_missing_skill(self):

        student = self.student.copy()
        student["skills"] = "Python;SQL"

        result = check_eligibility(
            student,
            self.job
        )

        self.assertEqual(result["score"], 66.67)
        self.assertFalse(result["eligible"])
        self.assertIn("fastapi", result["missing"])

    # Test 4: Programme mismatch
    def test_programme_mismatch(self):

        student = self.student.copy()
        student["programme"] = "BCA"

        result = check_eligibility(
            student,
            self.job
        )

        self.assertFalse(result["eligible"])
        self.assertIn(
            "Programme does not match",
            result["reasons"]
        )

    # Test 5: CGPA below requirement
    def test_low_cgpa(self):

        student = self.student.copy()
        student["cgpa"] = "6.0"

        result = check_eligibility(
            student,
            self.job
        )

        self.assertFalse(result["eligible"])
        self.assertIn(
            "CGPA below minimum requirement",
            result["reasons"]
        )

    # Test 6: Invalid CGPA during record validation
    def test_invalid_cgpa(self):

        student = self.student.copy()
        student["cgpa"] = "invalid"

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 7: CGPA outside valid range
    def test_cgpa_outside_range(self):

        student = self.student.copy()
        student["cgpa"] = "12"

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 8: Duplicate student ID
    def test_duplicate_student_id(self):

        student2 = self.student.copy()

        result = validate_records(
            [self.student, student2],
            "student"
        )

        self.assertEqual(len(result), 1)

    # Test 9: Invalid job CGPA
    def test_invalid_job_cgpa(self):

        job = self.job.copy()
        job["min_cgpa"] = "invalid"

        result = validate_records(
            [job],
            "job"
        )

        self.assertEqual(len(result), 0)

    # Test 10: Missing required fields
    def test_missing_student_fields(self):

        student = self.student.copy()
        student["name"] = ""

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 11: CSV missing required column
    def test_missing_csv_column(self):

        with tempfile.TemporaryDirectory() as folder:

            filename = os.path.join(
                folder,
                "students.csv"
            )

            with open(filename, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "student_id",
                    "name"
                ])

                writer.writerow([
                    "101",
                    "Rahul"
                ])

            result = read_csv_file(
                filename,
                [
                    "student_id",
                    "name",
                    "programme",
                    "cgpa",
                    "skills"
                ]
            )

            self.assertEqual(result, [])

    # Test 12: CSV file not found
    def test_missing_csv_file(self):

        result = read_csv_file(
            "nonexistent_test_file.csv",
            ["student_id"]
        )

        self.assertEqual(result, [])

    # Test 13: Empty skills
    def test_empty_skills(self):

        student = self.student.copy()
        student["skills"] = ""

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 14: NaN CGPA
    def test_nan_cgpa(self):

        student = self.student.copy()
        student["cgpa"] = "nan"

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 15: Infinite CGPA
    def test_infinite_cgpa(self):

        student = self.student.copy()
        student["cgpa"] = "inf"

        result = validate_records(
            [student],
            "student"
        )

        self.assertEqual(len(result), 0)

    # Test 16: CSV report generation
    def test_report_generation(self):

        with tempfile.TemporaryDirectory() as folder:

            original_directory = os.getcwd()

            try:

                os.chdir(folder)

                generate_report(
                    [self.student],
                    [self.job]
                )

                self.assertTrue(
                    os.path.exists("eligibility_report.csv")
                )

                with open(
                    "eligibility_report.csv",
                    "r",
                    newline=""
                ) as file:

                    reader = csv.DictReader(file)
                    rows = list(reader)

                self.assertEqual(len(rows), 1)

                self.assertEqual(
                    rows[0]["Eligibility Status"],
                    "MEETS CRITERIA"
                )

            finally:

                os.chdir(original_directory)

    # Test 17: Recursive function handles empty dictionary
    def test_empty_recursion(self):

        self.assertIsNone(display_skills({}))

    # Test 18: Recursive function handles nested dictionaries
    def test_nested_recursion(self):

        category = {
            "Programming": {
                "Python": {
                    "FastAPI": {}
                }
            }
        }

        self.assertIsNone(display_skills(category))


    # Test 19: Malformed CSV row with extra values
    def test_malformed_csv_extra_values(self):

        with tempfile.TemporaryDirectory() as folder:

            filename = os.path.join(folder, "students.csv")

            with open(filename, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "student_id",
                    "name",
                    "programme",
                    "cgpa",
                    "skills"
                ])

                writer.writerow([
                    "101",
                    "Rahul",
                    "MCA",
                    "8.5",
                    "Python;SQL"
                ])

                writer.writerow([
                    "102",
                    "Priya",
                    "MCA",
                    "7.8",
                    "Python;SQL",
                    "UnexpectedValue"
                ])

            result = read_csv_file(
                filename,
                [
                    "student_id",
                    "name",
                    "programme",
                    "cgpa",
                    "skills"
                ]
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["student_id"], "101")

    # Test 20: Duplicate CSV column names
    def test_duplicate_csv_columns(self):

        with tempfile.TemporaryDirectory() as folder:

            filename = os.path.join(folder, "students.csv")

            with open(filename, "w", newline="") as file:

                file.write(
                    "student_id,name,name,programme,cgpa,skills\n"
                )

                file.write(
                    "101,Rahul,Rahul,MCA,8.5,Python;SQL\n"
                )

            result = read_csv_file(
                filename,
                [
                    "student_id",
                    "name",
                    "programme",
                    "cgpa",
                    "skills"
                ]
            )

            self.assertEqual(result, [])

    # Test 21: Empty CSV file
    def test_empty_csv_file(self):

        with tempfile.TemporaryDirectory() as folder:

            filename = os.path.join(folder, "empty.csv")

            with open(filename, "w") as file:
                pass

            result = read_csv_file(
                filename,
                ["student_id"]
            )

            self.assertEqual(result, [])

    # Test 22: Recursive function with multiple branches
    def test_multiple_recursion_branches(self):

        category = {
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

        self.assertIsNone(display_skills(category))

    # Test 23: Recursive function with deeper nesting
    def test_deep_recursion(self):

        category = {
            "Programming": {
                "Python": {
                    "Web Development": {
                        "Backend": {
                            "FastAPI": {}
                        }
                    }
                }
            }
        }

        self.assertIsNone(display_skills(category))

if __name__ == "__main__":

    print("\n========== AUTOMATED TESTING ==========\n")

    unittest.main(verbosity=2)
