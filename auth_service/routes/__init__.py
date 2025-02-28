from fastapi import APIRouter

from routes.auth import router as auth_router
from routes.history import router as history_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(history_router)