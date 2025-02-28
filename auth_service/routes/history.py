from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from services.user import user_service

router = APIRouter()

@router.get("/history")
async def get_user_history(user_id: int, request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    history_list = await user_service.get_user_history(access_token=access_token, user_id=user_id)
    if not history_list:
        raise HTTPException(status_code=403, detail="Access denied")
    history_list = [
    {**entry, "date": entry["date"].strftime("%Y-%m-%d %H:%M:%S")} if "date" in entry else entry
    for entry in history_list
]
    return JSONResponse(content={"history": history_list})