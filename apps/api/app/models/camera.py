
import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
    Uuid
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.api.app.db.base import Base


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    camera_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    location_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("locations.id"),
        nullable=False
    )

    source_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    connection_status: Mapped[str] = mapped_column(
        String(20),
        default="unknown",
        nullable=False
    )

    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_health_check_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    location = relationship(
        "Location",
        back_populates="cameras"
    )
