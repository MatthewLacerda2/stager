import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from .associations import render_objects, render_groups

class Render(Base):
    __tablename__ = "renders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    camera_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"), nullable=True)
    image_url = Column(String, nullable=True)

    # Relationships
    camera = relationship("Camera", back_populates="renders")
    objects = relationship("BlenderObject", secondary=render_objects, back_populates="renders")
    groups = relationship("Group", secondary=render_groups, back_populates="renders")
