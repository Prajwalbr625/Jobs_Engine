from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from typing import Optional

@dataclass
class Job:
    title: str
    company: str
    location: str
    apply_url: str
    source_name: str
    experience_level: str = "Unknown"
    role_category: str = "Other"
    fetched_at: datetime = field(default_factory=datetime.now)
    job_hash: str = ""

    def __post_init__(self):
        # Allow passing existing hash, or generate if empty
        pass
        
    def generate_hash(self):
        raw_string = f"{self.title}{self.company}{self.location}{self.apply_url}"
        self.job_hash = hashlib.md5(raw_string.encode("utf-8")).hexdigest()
