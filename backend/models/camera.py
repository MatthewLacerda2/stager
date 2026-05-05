import uuid
from datetime import datetime
from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Camera(Base):
    __tablename__ = "cameras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fov = Column(Float, default=39.6)
    
    # Spatial
    pos_x = Column(Float, default=0.0)
    pos_y = Column(Float, default=0.0)
    pos_z = Column(Float, default=0.0)
    
    rot_x = Column(Float, default=0.0)
    rot_y = Column(Float, default=0.0)
    rot_z = Column(Float, default=0.0)
    
    scale_x = Column(Float, default=1.0)
    scale_y = Column(Float, default=1.0)
    scale_z = Column(Float, default=1.0)
    
    near = Column(Float, default=0.1)
    far = Column(Float, default=1000.0)
    aspect = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    renders = relationship("Render", back_populates="camera")
