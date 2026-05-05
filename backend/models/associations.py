from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

# Association table for Group and BlenderObject
group_objects = Table(
    "group_objects",
    Base.metadata,
    Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True),
    Column("object_id", UUID(as_uuid=True), ForeignKey("blender_objects.id"), primary_key=True),
)

# Association table for Render and BlenderObject
render_objects = Table(
    "render_objects",
    Base.metadata,
    Column("render_id", UUID(as_uuid=True), ForeignKey("renders.id"), primary_key=True),
    Column("object_id", UUID(as_uuid=True), ForeignKey("blender_objects.id"), primary_key=True),
)

# Association table for Render and Group
render_groups = Table(
    "render_groups",
    Base.metadata,
    Column("render_id", UUID(as_uuid=True), ForeignKey("renders.id"), primary_key=True),
    Column("group_id", UUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True),
)
