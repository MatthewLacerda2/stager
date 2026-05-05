import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .base import Base
from .associations import group_objects, render_objects

class BlenderObject(Base):
    __tablename__ = "blender_objects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=True)
    vtx_count = Column(Integer, nullable=True)
    
    # Complex 3D data
    hexa_prints = Column(JSONB, nullable=True)
    hexa_prints_embeddings = Column(JSONB, nullable=True)
    modifiers = Column(JSONB, nullable=True)
    materials = Column(JSONB, nullable=True)
    
    # Spatial data
    origin = Column(JSONB, nullable=True) # e.g., [x, y, z]
    boundbox = Column(JSONB, nullable=True) # e.g., [[min_x, ...], [max_x, ...]]
    radius = Column(Float, nullable=True)
    
    # Transformation
    pos_x = Column(Float, default=0.0)
    pos_y = Column(Float, default=0.0)
    pos_z = Column(Float, default=0.0)
    
    rot_x = Column(Float, default=0.0)
    rot_y = Column(Float, default=0.0)
    rot_z = Column(Float, default=0.0)
    
    scale_x = Column(Float, default=1.0)
    scale_y = Column(Float, default=1.0)
    scale_z = Column(Float, default=1.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships - using string names for classes to avoid circular imports
    groups = relationship("Group", secondary=group_objects, back_populates="objects")
    renders = relationship("Render", secondary=render_objects, back_populates="objects")