# SPDX-FileCopyrightText: 2026 Trần Trí Kiên
#
# SPDX-License-Identifier: Apache-2.0


from datetime import UTC, datetime

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class SensorPoint(Base):
    __tablename__ = "sensor_point"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ----- dữ liệu đọc từ file .ttl -----
    uri: Mapped[str] = mapped_column(String(300), unique=True)
    brick_class: Mapped[str] = mapped_column(String(120))
    label: Mapped[str | None] = mapped_column(String(200))
    unit: Mapped[str | None] = mapped_column(String(40))

    # ----- 6 cột dưới đây BẮT BUỘC, giữ đúng tên, đừng đổi -----
    source_dataset: Mapped[str] = mapped_column(String(80))
    source_url: Mapped[str] = mapped_column(String(400))
    source_license: Mapped[str] = mapped_column(String(40))
    source_checksum: Mapped[str] = mapped_column(String(80))
    transformation_version: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )


def make_session(db_path: str = "data.db"):
    engine = create_engine(f"sqlite+pysqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()