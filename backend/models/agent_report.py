import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from .base import Base

class AgenticLog(Base):
    __tablename__ = "agent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(String, nullable=True)

    order = Column(Integer)
    
    tool_name = Column(String, nullable=True)
    tool_args = Column(ARRAY(String))

    created_at = Column(DateTime, default=datetime.utcnow)