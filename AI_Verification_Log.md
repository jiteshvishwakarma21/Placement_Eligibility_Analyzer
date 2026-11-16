# AI Verification Log

## 1. Purpose

This document records how Artificial Intelligence (AI) assistance was used during the development of the Placement Eligibility and Skill-Gap Analyzer. It also describes the testing and verification performed to check the correctness of the implementation.

AI was used as a development and learning assistant. The final implementation was executed using Python, and project decisions were reviewed against the assignment requirements.

## 2. AI Assistance and Verification Record

| No. | Area | AI Assistance | Verification / Action Taken |
|---|---|---|---|
| 1 | Project structure | Assistance in organizing the Python project and its files. | Project files and sample CSV inputs were created and reviewed. |
| 2 | CSV processing | Assistance in implementing CSV reading and validation. | The application was executed using the supplied student and job CSV files. |
| 3 | Skill normalization | Assistance in designing case-insensitive skill comparison. | Skill normalization was checked through automated unit tests. |
| 4 | Eligibility calculation | Assistance in implementing programme, CGPA, and skill checks. | Eligibility results were examined using the sample records. |
| 5 | Skill-match scoring | Assistance in defining a percentage-based scoring formula. | The formula and a worked example were documented in scoring_formula.md. |
| 6 | Recursive function | Assistance in implementing recursive traversal of nested skill categories. | Empty, single-child, multiple-branch, and deeply nested recursion cases were tested. |
| 7 | Error handling | Assistance in handling missing files, invalid values, and malformed CSV records. | Validation scenarios were tested through the unit test suite. |
| 8 | Automated testing | Assistance in preparing Python unittest cases. | Executed `python3 -m unittest test_main -v`; all 23 tests passed. |
| 9 | Claim verification | Assistance in examining the five technical claims identified in the assignment. | Findings and verification limitations were documented in claim_verification.md. |
| 10 | Documentation | Assistance in preparing the scoring explanation and verification records. | Documentation files were reviewed for consistency with the implementation. |

## 3. Automated Testing Evidence

The following command was used to execute the automated tests:

```bash
python3 -m unittest test_main -v
```

**Recorded result: 23 tests passed successfully.**

The test suite covered:

- Skill normalization.
- All skills matched.
- Missing skills.
- Programme mismatch.
- CGPA eligibility and validation.
- Duplicate student IDs.
- Missing student information.
- Invalid numeric values, including NaN and infinity.
- Missing CSV files and required columns.
- Empty CSV files.
- Duplicate CSV column names.
- Malformed CSV rows containing extra values.
- CSV report generation.
- Empty recursion.
- Nested recursion.
- Multiple recursion branches.
- Deep recursion.

The test results were observed in the terminal during development.

## 4. Application Execution Verification

The application was executed using:

```bash
python3 main.py
```

The following results were observed:

- Five student records were loaded successfully.
- Three job records were loaded successfully.
- Fifteen student-job comparisons were performed.
- The eligibility report was generated successfully.
- Scoring information and eligibility conditions were displayed.
- Nested skill categories and recursion demonstrations were executed.

The generated `eligibility_report.csv` was inspected.

Recorded report results:

- Total comparisons: 15
- Eligible comparisons: 5
- Not eligible comparisons: 10

The module import behaviour was also checked using:

```bash
python3 -c "import main; print('IMPORT SUCCESSFUL')"
```

Only the expected import confirmation was displayed, without automatically executing the application.

## 5. Technical Claim Verification

Five technical claims specified in the assignment were examined and documented in `claim_verification.md`.

The verification document distinguishes between unsupported claims, claims contradicted by documented APIs, and claims that could not be conclusively verified.

The conclusions are limited to the evidence and references documented in that file.

## 6. Human Review and Responsibility

AI-generated suggestions were treated as assistance rather than automatically accepted as correct.

The following actions were performed during development:

- The Python application was executed locally.
- The generated eligibility report was examined.
- Automated unit tests were executed.
- The scoring formula was documented.
- Technical claims were recorded with their verification status.
- Project documentation was prepared to explain the implementation and its limitations.

The student remains responsible for understanding the code, checking the results, and ensuring that the submitted project meets the assignment requirements.

## 7. Ethical Considerations

The application uses only the information supplied in the student and job CSV files.

It does not infer skills or abilities from names, colleges, or personal backgrounds. Its output is based on explicit programme, CGPA, and listed-skill requirements.

The analyzer is intended as a decision-support tool and does not guarantee placement or replace human recruitment decisions.

## 8. Conclusion

AI assistance supported the development, testing, and documentation of this project. Local execution, report inspection, and automated testing provided practical checks of the implementation.

The verification process helped identify the limitations of the scoring method and reinforced the importance of transparent, evidence-based software development.