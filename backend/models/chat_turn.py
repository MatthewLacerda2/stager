import uuid
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class ChatTurn(Base):
    __tablename__ = "chat_turns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"))
    user_prompt = Column(Text, nullable=True)
    agent_response = Column(Text, nullable=True)
    #TODO: store token usage
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat = relationship("Chat", back_populates="chat_turns")
    agent_logs = relationship("AgentLog", back_populates="chat_turn")
