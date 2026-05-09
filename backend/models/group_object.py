import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class GroupObject(Base):
    __tablename__ = "group_objects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"))
    name = Column(String, nullable=True)
    
    pos_x = Column(Float)
    pos_y = Column(Float)
    pos_z = Column(Float)
    
    rot_x = Column(Float)
    rot_y = Column(Float)
    rot_z = Column(Float)
    
    scale_x = Column(Float)
    scale_y = Column(Float)
    scale_z = Column(Float)
    
    # Relationships
    scene = relationship("Scene", back_populates="group_objects")
    scene_objects = relationship("SceneObject", back_populates="group_object")
