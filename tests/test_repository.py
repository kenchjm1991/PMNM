# SPDX-FileCopyrightText: 2026 Trần Trí Kiên
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from src.loader import doc_diem_do, nap_vao_db
from src.models import make_session
from src.repository import SensorPointRepository


def test_chi_nap_diem_do_dung_loai(tmp_path):
    """File mẫu có 4 mục nhưng HVAC_Zone phải bị lọc bỏ."""
    session = make_session(str(tmp_path / "test.db"))
    diem_do = doc_diem_do(Path("tests/mau.ttl"))
    so_ban_ghi = nap_vao_db(session, diem_do, "checksum-test")
    assert so_ban_ghi == 3
    assert SensorPointRepository(session).count() == 3


def test_by_brick_class_chi_tra_ban_ghi_khop(tmp_path):
    session = make_session(str(tmp_path / "test.db"))
    nap_vao_db(session, doc_diem_do(Path("tests/mau.ttl")), "checksum-test")
    ket_qua = SensorPointRepository(session).by_brick_class("Temperature")
    assert len(ket_qua) == 2
    for diem in ket_qua:
        assert "Temperature" in diem.brick_class


def test_nap_hai_lan_khong_bi_trung(tmp_path):
    """Chạy lại lệnh nạp không được tạo bản ghi trùng."""
    session = make_session(str(tmp_path / "test.db"))
    diem_do = doc_diem_do(Path("tests/mau.ttl"))
    nap_vao_db(session, diem_do, "checksum-test")
    nap_vao_db(session, diem_do, "checksum-test")
    assert SensorPointRepository(session).count() == 3