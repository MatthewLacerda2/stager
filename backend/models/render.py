import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class Render(Base):
    __tablename__ = "renders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"))
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"))
    
    image_url = Column(String)
    description = Column(Text)
    description_embedding = Column(Vector(NUM_DIMENSIONS))
    image_embedding = Column(Vector(NUM_DIMENSIONS))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scene = relationship("Scene", back_populates="renders")
    camera = relationship("Camera", back_populates="renders")
