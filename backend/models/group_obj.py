import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from .base import Base
from ..utils.envs import NUM_DIMENSIONS

class GroupObj(Base):
    __tablename__ = "group_objs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)
    description_embedding = Column(Vector(NUM_DIMENSIONS))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    objects = relationship("BlenderObject", back_populates="group")
