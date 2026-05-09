import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base

class Modifier(Base):
    __tablename__ = "modifiers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_object_id = Column(UUID(as_uuid=True), ForeignKey("scene_objects.id"))
    execution_order = Column(Integer)
    type = Column(String)  # Blender default modifier name, e.g., ARRAY, BEVEL, MIRROR
    data = Column(JSONB)   # Arbitrary JSON payload for safe data application
    
    # Relationships
    scene_object = relationship("SceneObject", back_populates="modifiers")
