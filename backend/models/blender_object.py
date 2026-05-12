import uuid
from sqlalchemy import Column, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class BlenderObject(Base):
    __tablename__ = "blender_objects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)
    keywords = Column(ARRAY(String), nullable=False, server_default='{}')
    
    asset_path = Column(String, nullable=True)
    
    boundbox_x = Column(Float, nullable=True)
    boundbox_y = Column(Float, nullable=True)
    boundbox_z = Column(Float, nullable=True)
    boundbox_offset_x = Column(Float, nullable=True)
    boundbox_offset_y = Column(Float, nullable=True)
    boundbox_offset_z = Column(Float, nullable=True)
    
    radius = Column(Float, nullable=True)
    radius_offset_x = Column(Float, nullable=True)
    radius_offset_y = Column(Float, nullable=True)
    radius_offset_z = Column(Float, nullable=True)
    
    # Relationships
    scene_objects = relationship("SceneObject", back_populates="blender_object")