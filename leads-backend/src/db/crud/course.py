from sqlalchemy import asc, desc, text
from src.app.api.schemas import CourseDB
from src.db.base import course, database


async def get(id: int):
    course_query = course.select().where(id == course.c.id)

    return await database.fetch_one(query=course_query)


async def get_all(sort: str):
    sort = sort.strip("[]").split(",")
    sort_field = sort[0].strip('""')
    sort_direction = sort[1].upper().strip('""')

    if sort_direction == "ASC":
        order_clause = asc(text(sort_field))
    else:
        order_clause = desc(text(sort_field))
    course_query = course.select().order_by(order_clause)

    return await database.fetch_all(query=course_query)


async def get_filtered_courses(career_id: int, sort: str) -> list:
    sort = sort.strip("[]").split(",")
    sort_field = sort[0].strip('""')
    sort_direction = sort[1].upper().strip('""')

    if sort_direction == "ASC":
        order_clause = asc(text(sort_field))
    else:
        order_clause = desc(text(sort_field))

    query = (
        course.select().where(career_id == course.c.career_id).order_by(order_clause)
    )
    courses_result = await database.fetch_all(query=query)

    courses_data = []

    for course_result in courses_result:
        course_data = CourseDB(
            id=course_result.id,
            name=course_result.name,
        )
        courses_data.append(course_data)

    return courses_data
