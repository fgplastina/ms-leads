from fastapi import APIRouter
from src.app.api import career, course, lead

router = APIRouter()

router.include_router(lead.router, prefix="/leads", tags=["leads"])
router.include_router(course.router, prefix="/courses", tags=["courses"])
router.include_router(career.router, prefix="/careers", tags=["careers"])
