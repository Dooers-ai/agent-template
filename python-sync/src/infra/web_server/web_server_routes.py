from fastapi import APIRouter, HTTPException

from src.module.message_controller import router as message_router
from src.module.task_controller import router as task_router
from src.module.settings_controller import router as settings_router

router = APIRouter(prefix="/api")

router.include_router(message_router, prefix="/v1")
router.include_router(task_router, prefix="/v1")
router.include_router(settings_router, prefix="/v1")


@router.get("/{path:path}", include_in_schema=False)
async def not_found_handler():
    raise HTTPException(status_code=404, detail="endpoint not found")
