from fastapi import APIRouter, HTTPException

from src.module.agent_controller import router as agent_router

router = APIRouter(prefix="/api")

router.include_router(agent_router, prefix="/v1")


@router.get("/{path:path}", include_in_schema=False)
async def not_found_handler():
    raise HTTPException(status_code=404, detail="endpoint not found")
