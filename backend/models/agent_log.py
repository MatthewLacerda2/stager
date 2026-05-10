import uuid
from .base import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, String, DateTime, ForeignKey

class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_turn_id = Column(UUID(as_uuid=True), ForeignKey("chat_turns.id"))
    tool_call_id = Column(String, nullable=True)
    tool_name = Column(String, nullable=True)
    tool_input = Column(JSONB, nullable=True)
    tool_output = Column(JSONB, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat_turn = relationship("ChatTurn", back_populates="agent_logs")
