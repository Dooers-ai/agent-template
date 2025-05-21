from fastapi import APIRouter, HTTPException

from src.module.example.example_controller import router as example_router

router = APIRouter(prefix="/api")

router.include_router(example_router, prefix="/v1/example")


@router.get("/{path:path}", include_in_schema=False)
async def not_found_handler():
    raise HTTPException(status_code=404, detail="endpoint not found")
