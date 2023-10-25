from datetime import datetime

from sqlalchemy import and_, asc, desc, text
from src.app.api.schemas import (
    CourseDB,
    CourseSchema,
    LeadDB,
    LeadDetailedDB,
    LeadSchema,
)
from src.db.base import course, database, lead


async def get_all(sort: str):
    sort = sort.strip("[]").split(",")
    sort_field = sort[0].strip('""')
    sort_direction = sort[1].upper().strip('""')

    if sort_direction == "ASC":
        order_clause = asc(text(sort_field))
    else:
        order_clause = desc(text(sort_field))

    lead_query = lead.select().order_by(order_clause)
    leads_results = await database.fetch_all(query=lead_query)

    leads_data = []

    for lead_result in leads_results:
        courses_query = course.select().where(lead_result.id == course.c.lead_id)
        courses_result = await database.fetch_all(query=courses_query)
        lead_data = LeadDB(
            id=lead_result.id,
            first_name=lead_result.first_name,
            last_name=lead_result.last_name,
            email=lead_result.email,
            address=lead_result.address,
            phone=lead_result.phone,
            inscription_year=lead_result.inscription_year,
            career_id=lead_result.career_id,
            number_of_times_taken=lead_result.number_of_times_taken,
            created_date=lead_result.created_date,
            courses=[course.id for course in courses_result],
        )
        leads_data.append(lead_data)

    return leads_data


async def get(id: int):
    lead_query = lead.select().where(id == lead.c.id)
    courses_query = course.select().where(id == course.c.lead_id)

    lead_result = await database.fetch_one(query=lead_query)
    courses_result = await database.fetch_all(query=courses_query)

    if not lead_result:
        return None

    lead_data = LeadDB(
        id=lead_result.id,
        first_name=lead_result.first_name,
        last_name=lead_result.last_name,
        email=lead_result.email,
        address=lead_result.address,
        phone=lead_result.phone,
        inscription_year=lead_result.inscription_year,
        career_id=lead_result.career_id,
        number_of_times_taken=lead_result.number_of_times_taken,
        created_date=lead_result.created_date,
        courses=[course.id for course in courses_result],
    )

    return lead_data


async def post(payload: LeadSchema):
    #    courses = [
    #        CourseSchema(
    #            name=course.name,
    #        )
    #        for course in payload.courses
    #    ]

    lead_instance = LeadSchema(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        address=payload.address,
        phone=payload.phone,
        inscription_year=payload.inscription_year,
        career_id=payload.career_id,
        number_of_times_taken=payload.number_of_times_taken,
        courses=payload.courses,
    )

    query = lead.insert().values(
        first_name=lead_instance.first_name,
        last_name=lead_instance.last_name,
        email=lead_instance.email,
        address=lead_instance.address,
        phone=lead_instance.phone,
        inscription_year=lead_instance.inscription_year,
        career_id=lead_instance.career_id,
        number_of_times_taken=lead_instance.number_of_times_taken,
        created_date=datetime.now(),
    )

    lead_id = await database.execute(query=query)

    query_courses = (
        course.update()
        .where(course.c.id.in_(payload.courses))
        .values(
            lead_id=lead_id,
        )
    )

    await database.execute(query=query_courses)

    course_query = course.select().where(lead_id == course.c.lead_id)
    courses = await database.fetch_all(query=course_query)

    return lead_id, courses


async def patch(id: int, payload: dict):
    lead_query = lead.select().where(id == lead.c.id)
    lead_result = await database.fetch_one(query=lead_query)

    if not lead_result:
        return None

    lead_query = lead.update().where(id == lead.c.id).values(**payload)
    updated_rows = await database.execute(query=lead_query)

    if updated_rows == 0:
        return None

    for i in payload.get("courses", []):
        course_update_query = (
            course.update()
            .where(and_(id == course.c.lead_id, i.id == course.c.id))
            .values(
                product=i.product,
                description=i.description,
                price=i.price,
                quantity=i.quantity,
            )
        )
        await database.execute(query=course_update_query)

    lead_get_query = lead.select().where(id == lead.c.id)
    lead_data = await database.fetch_one(query=lead_get_query)

    course_query = course.select().where(id == course.c.lead_id)
    courses = await database.fetch_all(query=course_query)

    return lead_data, courses


async def put(id: int, payload: LeadDetailedDB):
    lead_update_query = (
        lead.update()
        .where(id == lead.c.id)
        .values(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            address=payload.address,
            phone=payload.phone,
            inscription_year=payload.inscription_year,
            career_id=payload.career_id,
            number_of_times_taken=payload.number_of_times_taken,
        )
        .returning(lead.c.id)
    )

    lead_id = await database.execute(query=lead_update_query)

    for i in payload.courses:
        course_update_query = (
            course.update()
            .where(and_(lead_id == course.c.lead_id, i.id == course.c.id))
            .values(
                name=i.name,
            )
        )
        await database.execute(query=course_update_query)

    lead_get_query = lead.select().where(lead_id == lead.c.id)
    lead_data = await database.fetch_one(query=lead_get_query)

    course_query = course.select().where(lead_id == course.c.lead_id)
    courses = await database.fetch_all(query=course_query)

    return lead_data, courses
