import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class ArrayModifier(Base):
    __tablename__ = "array_modifiers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_object_id = Column(UUID(as_uuid=True), ForeignKey("scene_objects.id"), unique=True)
    count = Column(Integer, default=2)
    offset_type = Column(String, default="relative") # 'relative' or 'constant'
    
    factor_x = Column(Float, default=1.0)
    factor_y = Column(Float, default=0.0)
    factor_z = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    scene_object = relationship("SceneObject", back_populates="array_modifier")
