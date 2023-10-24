import json
from typing import List

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from src.app.api.schemas import CourseDB
from src.db.crud import course as course_crud

router = APIRouter()


@router.get("/{id}/", response_model=CourseDB)
async def read_course(id: int = Path(..., gt=0)):
    course = await course_crud.get(id)

    if not course:
        return JSONResponse(status_code=404, content={"detail": "course not found"})

    return course


@router.get("/", response_model=List[CourseDB])
async def read_all_courses(
    range: str = Query(None, description="Range of pagination"),
    filter: str = Query("'career_id'", description="Filters"),
    sort: str = Query('["id", "ASC"]', description="Sort"),
):

    career_id = None

    if filter:
        # Analiza la cadena JSON en el parámetro "filter"
        filter_dict = json.loads(filter)
        career_id = filter_dict.get("career_id", None)

    if career_id:
        courses = await course_crud.get_filtered_courses(career_id,sort)
    else:
        courses = await course_crud.get_all(sort)

    total_courses = len(courses)
    range_start, range_end = None, None
    if range:
        try:
            range_start, range_end = map(int, range.strip("[]").split(","))
            range_end += 1
        except ValueError:
            return JSONResponse(
                status_code=400, content={"detail": "Range format is incorrect."}
            )

    content_range_header = f"{range_start}-{range_end}/{total_courses}"

    response_headers = {
        "Access-Control-Expose-Headers": "Content-Range",
        "Content-Range": content_range_header,
        "X-Total-Count": "10",
    }

    ranged_courses = courses[range_start:range_end]
    paginated_courses = [{"id": course.id, "name": course.name} for course in ranged_courses]

    return JSONResponse(content=paginated_courses, headers=response_headers)
