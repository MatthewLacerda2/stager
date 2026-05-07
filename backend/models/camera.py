import uuid
from datetime import datetime
from sqlalchemy import Column, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from .base import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fov = Column(Float)
    
    # Spatial
    pos = Column(ARRAY(Float))
    rot = Column(ARRAY(Float))
    scale = Column(ARRAY(Float))
    
    near = Column(Float)
    far = Column(Float)
    width = Column(Integer)
    height = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    renders = relationship("Render", back_populates="camera")
