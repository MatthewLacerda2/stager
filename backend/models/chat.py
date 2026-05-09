import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scene = relationship("Scene", back_populates="chats")
    chat_turns = relationship("ChatTurn", back_populates="chat")
