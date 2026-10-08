from fastapi import APIRouter, Depends

from app.dependencies import require_role


router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def admin_dashboard(
    current_user=Depends(require_role("ADMIN"))
):
    return {
        "message": "Admin dashboard",
        "admin": current_user.username,
    }