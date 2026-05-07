import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from .base import Base

class Light(Base):
    __tablename__ = "lights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    light_type = Column(Enum('sun', 'point', 'spot', 'area', name='light_type_enum'))
    
    # Spatial
    pos = Column(ARRAY(Float))
    rot = Column(ARRAY(Float))
    scale = Column(ARRAY(Float))
    
    color = Column(String)
    intensity = Column(Float)
    radius = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
