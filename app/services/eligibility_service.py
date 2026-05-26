from app.models.degree_requirement import DegreeRequirement
from app.models.requirement_group import RequirementGroup
from app.models.group_subject import GroupSubject
from app.models.student_result import StudentResult
from app.models.degree_program import DegreeProgram


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


def find_degrees_by_subjects(db, subject_ids):
    """
    Find degree programs whose requirement templates mention ALL subject_ids passed.

    Simple algorithm:
    - For each degree, load its DegreeRequirement to get the template_id
    - Collect all subject_ids referenced by GroupSubject for that template
    - If the provided subject_ids are a subset of that set, the degree is considered
      compatible and is returned.

    This is intentionally simple and easy to understand. For large datasets you
    may want to convert this to a single SQL query with joins and GROUP BY.

    Args:
        db: SQLAlchemy session
        subject_ids: iterable of subject id integers

    Returns:
        list of `DegreeProgram` objects that match
    """

    # normalize input to a set for fast membership tests
    required_set = set(int(s) for s in subject_ids if s is not None)

    if not required_set:
        return []

    degrees = db.query(DegreeProgram).all()
    matches = []

    for degree in degrees:
        # load degree requirement to get the template that groups reference
        degree_requirement = db.query(DegreeRequirement).filter(
            DegreeRequirement.degree_id == degree.degree_id
        ).first()

        if not degree_requirement:
            # if no requirement template, we cannot match subjects -- skip
            continue

        # collect all subject ids referenced by groups for this template
        group_subjects = db.query(GroupSubject).join(
            RequirementGroup,
            GroupSubject.group_id == RequirementGroup.group_id
        ).filter(
            RequirementGroup.template_id == degree_requirement.template_id
        ).all()

        template_subject_set = set(gs.subject_id for gs in group_subjects)

        # if all provided subjects are present in the template, it's a match
        if required_set.issubset(template_subject_set):
            matches.append(degree)

    return matches