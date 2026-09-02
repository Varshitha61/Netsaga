from pydantic import BaseModel, Field
from typing import List, Literal

FAULT_CATEGORIES = Literal[
    "VLAN Misconfiguration",
    "Default Gateway Issues",
    "DHCP Failure",
    "DNS Failure",
    "Routing Problems",
    "ACL Blocking",
    "NAT Misconfiguration",
    "Wireless / SSID Security Issues",
    "Unknown"
]

class DiagnosisResult(BaseModel):
    diagnosis: str = Field(..., description="Short summary of the issue.")
    fault_category: FAULT_CATEGORIES = Field(..., description="The category of the fault.")
    evidence: List[str] = Field(..., description="List of evidence strings derived from command outputs.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0.")
    recommended_fix: str = Field(..., description="Exact CLI commands or actions to resolve the issue.")
