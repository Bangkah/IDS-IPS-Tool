from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["ml"])

# Placeholder for ML analytics endpoints
@router.get("/ml/analytics")
def ml_analytics():
    return {"msg": "ML analytics endpoint (implementasi selanjutnya)"}
