from pydantic import BaseModel


class ReportSummary(BaseModel):

    total_scans: int

    safe: int

    suspicious: int

    dangerous: int