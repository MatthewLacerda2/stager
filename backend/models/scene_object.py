import uuid
from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class SceneObject(Base):
    __tablename__ = "scene_objects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"))
    blender_object_id = Column(UUID(as_uuid=True), ForeignKey("blender_objects.id"))
    group_object_id = Column(UUID(as_uuid=True), ForeignKey("group_objects.id"), nullable=True)
    
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
    scene = relationship("Scene", back_populates="scene_objects")
    blender_object = relationship("BlenderObject", back_populates="scene_objects")
    group_object = relationship("GroupObject", back_populates="scene_objects")
    array_modifier = relationship("ArrayModifier", back_populates="scene_object", uselist=False)