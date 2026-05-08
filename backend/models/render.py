import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class Render(Base):
    __tablename__ = "renders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    description_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    cam_id = Column(UUID(as_uuid=True), ForeignKey("cameras.id"))
    image_url = Column(String, unique=True)

    # Relationships
    camera = relationship("Camera", back_populates="renders")
