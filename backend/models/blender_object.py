import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class BlenderObject(Base):
    __tablename__ = "blender_objects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, nullable=True)
    description_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)
    
    # Spatial data
    boundbox = Column(ARRAY(Float))
    boundbox_offset = Column(ARRAY(Float))
    radius = Column(Float)
    radius_offset = Column(ARRAY(Float))
    
    # Transformation
    pos = Column(ARRAY(Float))
    rot = Column(ARRAY(Float))
    scale = Column(ARRAY(Float))
    
    group_id = Column(UUID(as_uuid=True), ForeignKey("group_objs.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    group = relationship("GroupObj", back_populates="objects")