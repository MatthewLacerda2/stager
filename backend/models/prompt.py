import uuid
from .base import Base
from datetime import datetime
from pgvector.sqlalchemy import Vector
from ..utils.envs import NUM_DIMENSIONS
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=True)
    text_embedding = Column(Vector(NUM_DIMENSIONS), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)