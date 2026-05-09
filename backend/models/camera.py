import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"))
    name = Column(String, nullable=True)
    
    pos_x = Column(Float)
    pos_y = Column(Float)
    pos_z = Column(Float)
    
    rot_x = Column(Float)
    rot_y = Column(Float)
    rot_z = Column(Float)
    
    fov = Column(Float)
    is_active = Column(Boolean, default=False)
    
    # Relationships
    scene = relationship("Scene", back_populates="cameras")
    renders = relationship("Render", back_populates="camera")
