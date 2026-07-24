from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_scans: int
    safe: int
    warning: int
    dangerous: int
    average_risk: float