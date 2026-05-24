from app.models.degree_requirement import DegreeRequirement
from app.models.requirement_group import RequirementGroup
from app.models.group_subject import GroupSubject
from app.models.student_result import StudentResult


GRADE_RANK = {
    "A": 5,
    "B": 4,
    "C": 3,
    "S": 2,
    "F": 1
}

def normalize_grade(grade):

    if grade is None:
        return None

    return grade.strip().upper()

def check_subject_requirements(

    db,
    student_profile,
    degree_id

):

    degree_requirement = db.query(
        DegreeRequirement
    ).filter(

        DegreeRequirement.degree_id == degree_id

    ).first()

    if not degree_requirement:

        return True

    student_subjects = db.query(
        StudentResult
    ).filter(

        StudentResult.student_id == student_profile.student_id

    ).all()

    student_subject_map = {}

    for subject in student_subjects:

        student_subject_map[subject.subject_id] = subject.grade

    groups = db.query(
        RequirementGroup
    ).filter(

        RequirementGroup.template_id == degree_requirement.template_id

    ).all()

    for group in groups:

        matched_subjects = 0

        group_subjects = db.query(
            GroupSubject
        ).filter(

            GroupSubject.group_id == group.group_id

        ).all()

        for subject in group_subjects:

            student_grade = normalize_grade(
                student_subject_map.get(subject.subject_id)
            )
            required_grade = normalize_grade(subject.required_grade)

            if student_grade and required_grade:
                if GRADE_RANK.get(student_grade, 0) >= GRADE_RANK.get(required_grade, 0):
                    matched_subjects += 1

        if matched_subjects < group.minimum_required:

            return False

    return True