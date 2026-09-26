# ofdx-sensor-points


Đọc file Brick TTL của LBNL và nạp danh sách điểm đo vào SQLite.



## Nguồn dữ liệu
- Tên: LBNL FDD RTU — Brick Schema TTL
- Link: https://fdddata.lbl.gov/data/Simulated_LBNL_FDD_Data_Sets_RTU/LBNL_FDD_Data_Sets_RTU_ttl.zip
- Giấy phép: CC BY 4.0
- Đã lọc: chỉ giữ loại chứa Sensor / Temperature / Pressure / Power


## Cách cài
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt



## Cách chạy
python -m src.main


## Kết quả
Đã nạp 0 điểm đo
Tổng trong database: 67
Checksum: 622978d1bd8c3efed40b5e705f73cb77be9202ae075cdffe6fce7fe36d77f5dc
Đếm theo loại:
  Discharge_Air_Temperature_Sensor: 1
  Electrical_Power_Sensor: 16
  Mixed_Air_Temperature_Sensor: 1
  Outside_Air_Flow_Sensor: 1
  Outside_Air_Humidity_Sensor: 1
  Outside_Air_Temperature_Sensor: 1
  Pressure_Sensor: 3
  Return_Air_Flow_Sensor: 1
  Return_Air_Humidity_Sensor: 1
  Return_Air_Temperature_Sensor: 1
  Supply_Air_Flow_Sensor: 1
  Supply_Air_Humidity_Sensor: 1
  Supply_Air_Temperature_Sensor: 11
  Temperature_Sensor: 2
  Zone_Air_Cooling_Temperature_Setpoint: 1
  Zone_Air_Heating_Temperature_Setpoint: 1
  Zone_Air_Humidity_Sensor: 11
  Zone_Air_Temperature_Sensor: 11
  Zone_Air_Temperature_Setpoint: 1