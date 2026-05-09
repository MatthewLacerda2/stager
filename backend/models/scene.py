import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class Scene(Base):
    __tablename__ = "scenes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    brief_description = Column(String(255), nullable=True)
    brief_description_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)
    detailed_description = Column(Text, nullable=True)
    detailed_description_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chats = relationship("Chat", back_populates="scene")
    group_objects = relationship("GroupObject", back_populates="scene")
    scene_objects = relationship("SceneObject", back_populates="scene")
    lights = relationship("Light", back_populates="scene")
    cameras = relationship("Camera", back_populates="scene")
    renders = relationship("Render", back_populates="scene")