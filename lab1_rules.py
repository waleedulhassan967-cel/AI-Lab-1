# Lab 1 Task 2
# All thresholds below are synthetic assumptions for this lab exercise.

def scholarship_check(score, documents_complete, attendance, form_verified):
    if (documents_complete and score >= 70
            and attendance >= 75 and form_verified):
        return "Review"
    return "Hold"


tests = [
    {
        "name": "all_conditions_pass",
        "inputs": (82, True, 80, True),
        "expected": "Review",
        "reason": "All four conditions are satisfied."
    },
    {
        "name": "attendance_condition_fails",
        "inputs": (82, True, 70, True),
        "expected": "Hold",
        "reason": "Attendance is below the synthetic 75% threshold."
    },
    {
        "name": "form_verification_fails",
        "inputs": (82, True, 80, False),
        "expected": "Hold",
        "reason": "The application form is not verified."
    },
    {
        "name": "score_boundary",
        "inputs": (70, True, 80, True),
        "expected": "Review",
        "reason": "Score is exactly 70 and the other conditions pass."
    }
]

print("CASE | INPUT | EXPECTED | ACTUAL | REASON")
for test in tests:
    actual = scholarship_check(*test["inputs"])
    print(
        test["name"], "|", test["inputs"], "|",
        test["expected"], "|", actual, "|", test["reason"]
    )
    assert actual == test["expected"], f"Test failed: {test['name']}"

print("\nAll four core test cases passed.")
