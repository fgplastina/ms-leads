from src.app.api.schemas import CareerDB, CourseDB
from src.db.base import career, course, database


async def get(id: int):
    career_query = career.select().where(id == career.c.id)
    courses_query = course.select().where(id == course.c.career_id)

    career_result = await database.fetch_one(query=career_query)
    courses_result = await database.fetch_all(query=courses_query)

    if not career_result:
        return None

    career_data = CareerDB(
        id=career_result.id,
        name=career_result.name,
        courses=[CourseDB(id=course.id, name=course.name) for course in courses_result],
    )

    return career_data


async def get_all():
    careers_query = career.select()

    careers_result = await database.fetch_all(query=careers_query)

    careers_data = []

    for career_result in careers_result:
        courses_query = course.select().where(career_result.id == course.c.career_id)
        courses_result = await database.fetch_all(query=courses_query)
        career_data = CareerDB(
            id=career_result.id,
            name=career_result.name,
            courses=[
                CourseDB(id=course.id, name=course.name) for course in courses_result
            ],
        )
        careers_data.append(career_data)

    return careers_data
