from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class IngestRecord(BaseModel):
    # Canonical schema after mapping
    external_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None

class AIResult(BaseModel):
    sentiment: Optional[str] = None
    category: Optional[str] = None
    risk_score: Optional[float] = None
    extra: Optional[Dict[str, Any]] = None

class ProcessRequest(BaseModel):
    records: List[IngestRecord]
