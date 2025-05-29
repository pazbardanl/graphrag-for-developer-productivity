from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class PREventDto(BaseModel):
    """
    Represents a simplified pull request event (either 'opened' or 'review submitted')
    in a unified format for ingestion, processing, and Kafka production.
    """
    action: str
    repo_name: str
    sender: str
    pr_number: int
    pr_user: str
    pr_files_changed: List[str] = Field(default_factory=list)
    review_user: Optional[str] = None
    review_state: Optional[str] = None
    review_submitted_at: Optional[datetime] = None