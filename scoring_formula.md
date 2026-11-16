# Scoring Formula and Eligibility Logic

## 1. Overview

The Placement Eligibility and Skill-Gap Analyzer evaluates how closely a student's listed skills match the skills required by a job.

The system calculates a transparent skill-match percentage and separately checks the eligibility criteria defined for each job.

## 2. Skill-Match Scoring Formula

The project uses the following formula:

**Skill Match Score = (Number of Matched Skills / Total Required Skills) × 100**

Where:

- **Matched Skills:** Skills that appear in both the student's skill list and the job's required skill list.
- **Total Required Skills:** Total number of skills specified by the job.

The result is expressed as a percentage.

## 3. Example Calculation

Consider the following example:

**Student skills:**
- Python
- SQL

**Job-required skills:**
- Python
- SQL
- FastAPI

The matched skills are Python and SQL.

Therefore:

Skill Match Score = (2 / 3) × 100

**Skill Match Score = 66.67%**

The missing skill is FastAPI.

## 4. Eligibility Conditions

A student is considered eligible only when all the following conditions are satisfied:

1. The student's programme matches the required job programme.
2. The student's CGPA is equal to or greater than the minimum CGPA required by the job.
3. The student possesses all the skills required by the job.

If any condition is not satisfied, the student is marked as not eligible.

## 5. Skill Normalization

Before comparing skills, the system:

- Removes unnecessary leading and trailing spaces.
- Converts skill names to lowercase.
- Removes duplicate skills.

For example:

`Python; SQL; FastAPI; python`

After normalization:

`python, sql, fastapi`

This ensures that differences in capitalization and duplicate entries do not affect the comparison.

## 6. Matched and Missing Skills

The system identifies:

- **Matched Skills:** Skills available in both student and job profiles.
- **Missing Skills:** Skills required by the job but not listed in the student's profile.

These results help students understand which additional skills they may need to develop.

## 7. Important Limitations

- The score measures only the overlap between listed skills; it does not measure actual technical proficiency.
- The system does not evaluate communication skills, interview performance, practical experience, or aptitude.
- The system does not infer skills from a student's name, college, background, or other personal characteristics.
- Eligibility depends on the information provided in the input CSV files.
- A high skill-match score does not automatically guarantee eligibility because programme and CGPA conditions must also be satisfied.
- The system is a basic decision-support tool and does not replace an employer's final recruitment decision.

## 8. Conclusion

The scoring method provides a simple, understandable, and transparent way to compare student skills with job requirements. By displaying matched skills, missing skills, and unmet eligibility conditions, the analyzer helps students identify skill gaps and understand job requirements.