# SPDX-FileCopyrightText: 2026 Trần Trí Kiên
#
# SPDX-License-Identifier: Apache-2.0

from abc import ABC, abstractmethod

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import SensorPoint


class Repository(ABC):
    """Lớp nền. Mọi repository đều nhận session và có ít nhất get() với count()."""

    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def get(self, record_id: int): ...

    @abstractmethod
    def count(self) -> int: ...


class SensorPointRepository(Repository):
    def get(self, record_id: int) -> SensorPoint | None:
        return self.session.get(SensorPoint, record_id)

    def count(self) -> int:
        return self.session.scalar(select(func.count()).select_from(SensorPoint)) or 0

    def by_brick_class(self, name: str) -> list[SensorPoint]:
        """Trả về các điểm đo thuộc một loại, ví dụ 'Temperature_Sensor'."""
        # Gợi ý: dùng .icontains(name) trên cột brick_class
        return list(
            self.session.scalars(
                select(SensorPoint).where(SensorPoint.brick_class.icontains(name)).order_by(SensorPoint.brick_class, SensorPoint.uri)
            )
        )

    def count_by_brick_class(self) -> dict[str, int]:
        """Đếm số điểm đo theo loại.

        Kết quả mong đợi trông giống:
        {"Temperature_Sensor": 8, "Pressure_Sensor": 4, ...}
        """
        rows = self.session.execute(
            select(SensorPoint.brick_class, func.count()).group_by(SensorPoint.brick_class)
        ).all()
        return {str(loai): int(so_luong) for loai, so_luong in rows}
