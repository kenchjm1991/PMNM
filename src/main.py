# SPDX-FileCopyrightText: 2026 Trần Trí Kiên
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from .loader import SOURCE_URL, doc_diem_do, giai_nen, nap_vao_db, tai_file, tinh_checksum
from .models import make_session
from .repository import SensorPointRepository

if __name__ == "__main__":
    session = make_session()
    zip_path = tai_file(SOURCE_URL, Path("data/raw/ttl.zip"))
    checksum = tinh_checksum(zip_path)
    ttl_files = giai_nen(zip_path, Path("data/extracted"))

    tong = 0
    for ttl in ttl_files:
        diem_do = doc_diem_do(ttl)
        tong += nap_vao_db(session, diem_do, checksum)

    repo = SensorPointRepository(session)
    print(f"Đã nạp {tong} điểm đo")
    print(f"Tổng trong database: {repo.count()}")
    print(f"Checksum: {checksum}")
    print("Đếm theo loại:")
    for loai, so_luong in repo.count_by_brick_class().items():
        print(f"  {loai}: {so_luong}")