# SPDX-FileCopyrightText: 2026 Trần Trí Kiên
#
# SPDX-License-Identifier: Apache-2.0


import hashlib
import zipfile
from pathlib import Path

import httpx
import rdflib
from rdflib.namespace import RDF, RDFS

from .models import SensorPoint

SOURCE_URL = (
    "https://fdddata.lbl.gov/data/Simulated_LBNL_FDD_Data_Sets_RTU/"
    "LBNL_FDD_Data_Sets_RTU_ttl.zip"
)
LICENSE = "CC-BY-4.0"
DATASET = "lbnl-fdd-rtu-ttl"
TRANSFORM = "brick-map-v1"

# Chỉ giữ điểm đo có loại chứa một trong các chữ này
TU_KHOA_CAN_LAY = ("Sensor", "Temperature", "Pressure", "Power")


def tai_file(url: str, dest: Path) -> Path:
    """Tải file về. Nếu đã có sẵn thì không tải lại."""
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, follow_redirects=True, timeout=300) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_bytes(1024 * 1024):
                f.write(chunk)
    return dest


def tinh_checksum(path: Path) -> str:
    """Mã sha256 của file — dùng để chứng minh file không bị đổi."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def giai_nen(zip_path: Path, dest_dir: Path) -> list[Path]:
    """Giải nén, trả về danh sách các file .ttl bên trong."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest_dir)
    return sorted(dest_dir.rglob("*.ttl"))


def doc_diem_do(ttl_path: Path) -> list[dict]:
    """Đọc file .ttl, trả về list các dict có 4 khóa: uri, brick_class, label, unit."""
    # phần này bạn viết
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")
    ket_qua = []

    for chu_ngu, _, loai in g.triples((None, RDF.type, None)):
        ten_loai = str(loai).rsplit("#", 1)[-1]   # bỏ phần đầu dài dòng của URL
        tukhoa = False
        for tk in TU_KHOA_CAN_LAY:
            if tk in ten_loai:
                tukhoa = True
                break
        if not tukhoa:
            continue        
        label = g.value(chu_ngu, RDFS.label)
        unit = None 
        ket_qua.append({
            "uri": str(chu_ngu),
            "brick_class": ten_loai,
            "label": str(label) if label else None,
            "unit": str(unit) if unit else None,})
        
    return ket_qua 



def nap_vao_db(session, diem_do: list[dict], checksum: str) -> int:
    """Tạo object SensorPoint từ list dict, lưu vào database. Trả về số bản ghi."""
    # phần này bạn viết
    so_lan_them = 0
    for diemdo in diem_do:
        tim_thay = session.query(SensorPoint).filter_by(uri=diemdo["uri"]).first()
        if tim_thay is not None:
            continue

        newobject = SensorPoint(
            uri=diemdo["uri"],
            brick_class=diemdo["brick_class"],
            label=diemdo["label"],
            unit=diemdo["unit"],
            source_dataset=DATASET,
            source_url=SOURCE_URL,
            source_license=LICENSE,
            source_checksum=checksum,
            transformation_version=TRANSFORM,
        )
        session.add(newobject)
        so_lan_them +=1
    session.commit()
    return so_lan_them
            
    