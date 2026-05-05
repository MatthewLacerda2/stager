import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Light(Base):
    __tablename__ = "lights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, default="POINT")
    
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
    
    color = Column(String, default="#FFFFFF")
    intensity = Column(Float, default=10.0)
    radius = Column(Float, default=1.0)
    falloff = Column(Float, default=1.0)

    created_at = Column(DateTime, default=datetime.utcnow)
