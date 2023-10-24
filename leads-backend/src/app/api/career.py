from typing import List

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from src.app.api.schemas import CareerDB
from src.db.crud import career as career_crud

router = APIRouter()


@router.get("/{id}/", response_model=CareerDB)
async def read_career(id: int = Path(..., gt=0)):
    career = await career_crud.get(id)

    if not career:
        return JSONResponse(status_code=404, content={"detail": "career not found"})

    return career


@router.get("/", response_model=List[CareerDB])
async def read_all_careers(
    range: str = Query(None, description="Range of pagination"),
    filter: str = Query(None, description="Filters"),
    sort: str = Query('["id", "ASC"]', description="Sort"),
):
    careers = await career_crud.get_all()

    total_career = len(careers)
    range_start, range_end = None, None
    if range:
        try:
            range_start, range_end = map(int, range.strip("[]").split(","))
            range_end += 1
        except ValueError:
            return JSONResponse(
                status_code=400, content={"detail": "Range format is incorrect."}
            )

    content_range_header = f"{range_start}-{range_end}/{total_career}"

    response_headers = {
        "Access-Control-Expose-Headers": "Content-Range",
        "Content-Range": content_range_header,
        "X-Total-Count": "10",
    }

    ranged_careers = careers[range_start:range_end]
    paginated_careers = [career.as_dict() for career in ranged_careers]

    return JSONResponse(content=paginated_careers, headers=response_headers)
