# 05_continuous_training_and_monitoring.md

## Huấn luyện Liên tục và Giám sát (Continuous Training & Monitoring)

Giai đoạn cuối cùng liên quan đến việc duy trì hệ thống: xử lý luồng dữ liệu mới (Continuous Training) và áp dụng các kỹ thuật theo dõi phân phối dữ liệu (Data Drift).

### Technical Checklist
- [ ] Chạy luồng bổ sung dữ liệu (`add_new_data.py`) và thực hiện quy trình DVC push.
- [ ] Theo dõi thí nghiệm trên DagsHub (Bonus).
- [ ] Tích hợp tính năng phát hiện trôi dạt dữ liệu (Data Drift Detection) vào luồng MLOps.

### 1. Cập nhật Mô hình với Dữ liệu Mới

Khi có dữ liệu mới tới, chúng ta cần chạy kịch bản để mở rộng tập dữ liệu hiện tại, đồng bộ hóa chúng với DVC và kích hoạt lại pipeline tự động.

```bash
# Generate and add new data
python add_new_data.py

# Track the updated dataset
dvc add data/wine_quality.csv

# Push new dataset to GCP
dvc push

# Commit to Git to trigger GitHub Actions
git add data/wine_quality.csv.dvc
git commit -m "CT: Append new data for model retraining"
git push origin main
```
Pipeline CI/CD (train_and_eval) sẽ tự động chạy và đánh giá mô hình trên phiên bản dữ liệu mới.

### 2. Tích hợp DagsHub (Bonus Challenge)

Thay vì thiết lập máy chủ MLflow nội bộ, hãy sử dụng dịch vụ lưu trữ miễn phí của DagsHub.
- Đăng nhập vào [DagsHub](https://dagshub.com/), kết nối với GitHub repository của dự án.
- Sao chép MLflow Tracking URI được cung cấp.
- Đặt URI này vào `MLFLOW_TRACKING_URI` ở cả môi trường local (`.env`) và GitHub Secrets.

### 3. Phát hiện Trôi dạt Dữ liệu - Data Drift (Bonus Challenge)

Theo dõi sự thay đổi phân phối của dữ liệu đầu vào trong quá trình sử dụng thực tế (Production) so với tập huấn luyện (Baseline). Sử dụng thư viện như `evidently` hoặc `alibi-detect`.

**Boilerplate Drift Detection (`src/drift_monitor.py`):**

```python
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_data_drift(reference_path: str, current_path: str):
    # TODO: Load reference (training) and current (production) data
    reference_data = pd.read_csv(reference_path)
    current_data = pd.read_csv(current_path)
    
    # Initialize Report
    report = Report(metrics=[DataDriftPreset()])
    
    # Run the report
    report.run(reference_data=reference_data, current_data=current_data)
    
    # TODO: Output the report to HTML or JSON
    report.save_html("drift_report.html")
    
    # Optional: Parse JSON to alert if Drift is detected
    
if __name__ == "__main__":
    check_data_drift("data/wine_quality_baseline.csv", "data/wine_quality_new.csv")
```
Thêm lệnh chạy kịch bản này vào GitHub Actions Workflow nếu bạn muốn ngăn chặn việc triển khai khi phát hiện Drift.
