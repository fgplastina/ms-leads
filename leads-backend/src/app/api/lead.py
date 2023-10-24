import datetime
import json
from typing import List

from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from src.app.api.schemas import LeadDB, LeadDetailedDB, LeadSchema
from src.db.crud import lead as lead_crud

router = APIRouter()


@router.post("/", response_model=LeadDB, status_code=201)
async def create_lead(payload: LeadSchema):
    lead_id, courses = await lead_crud.post(payload)
    lead = await lead_crud.get(lead_id)
    response_object = {
        "id": lead_id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "address": payload.address,
        "phone": payload.phone,
        "inscription_year": payload.inscription_year,
        "career_id": payload.career_id,
        "number_of_times_taken": payload.number_of_times_taken,
        "created_date": lead.created_date,
        "courses": [course for course in courses],
    }
    return response_object


@router.get("/{id}/", response_model=LeadDB)
async def read_lead(id: int = Path(..., gt=0)):
    lead = await lead_crud.get(id)

    if not lead:
        return JSONResponse(status_code=404, content={"detail": "Lead not found"})

    return lead


@router.get("/", response_model=List[LeadDB])
async def read_all_leads(
    range: str = Query(None, description="Range of pagination"),
    filter: str = Query(None, description="Filters"),
    sort: str = Query('["id", "ASC"]', description="Sort"),
):
    start_date = None
    end_date = None

    # Verifica si se proporciona el parámetro "range"
    if filter:
        # Analiza la cadena JSON en el parámetro "filter"
        filter_dict = json.loads(filter)
        start_date = filter_dict.get("start_date", None)
        end_date = filter_dict.get("end_date", None)
    try:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise JSONResponse(
            status_code=400, detail="Date format is incorrect. Use YYYY-MM-DD."
        )

    leads = []

    if start_date and end_date:
        leads = await lead_crud.get_filtered_leads(start_date, end_date, sort)
    else:
        leads = await lead_crud.get_all(sort)

    total_leads = len(leads)

    range_start, range_end = None, None

    if range:
        try:
            range_start, range_end = map(int, range.strip("[]").split(","))
            range_end += 1
        except ValueError:
            return JSONResponse(
                status_code=400, content={"detail": "Range format is incorrect."}
            )

    content_range_header = f"{range_start}-{range_end}/{total_leads}"

    response_headers = {
        "Access-Control-Expose-Headers": "Content-Range",
        "Content-Range": content_range_header,
        "X-Total-Count": "10",
    }

    ranged_leads = leads[range_start:range_end]
    paginated_leads = [lead.as_dict() for lead in ranged_leads]

    return JSONResponse(content=paginated_leads, headers=response_headers)


@router.put("/{id}/", response_model=LeadDB)
async def update_lead(id: int, payload: LeadDetailedDB):
    lead = await lead_crud.get(id)
    if not lead:
        return JSONResponse(status_code=404, content={"detail": "lead not found"})

    lead, courses = await lead_crud.put(id, payload)

    response_object = {
        "id": lead.id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "address": payload.address,
        "phone": payload.phone,
        "inscription_year": payload.inscription_year,
        "career_id": payload.career_id,
        "number_of_times_taken": payload.number_of_times_taken,
        "created_date": lead.created_date,
        "courses": [course for course in courses],
    }
    return response_object
