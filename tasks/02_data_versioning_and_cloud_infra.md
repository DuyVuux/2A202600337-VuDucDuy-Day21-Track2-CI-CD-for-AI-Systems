# 02_data_versioning_and_cloud_infra.md

## Phiên bản hóa Dữ liệu và Hạ tầng Đám mây (Data Versioning & Cloud Infra)

Tài liệu này tập trung vào việc quản lý phiên bản dữ liệu máy học bằng Data Version Control (DVC) và thiết lập kho lưu trữ từ xa (remote storage) trên Google Cloud Platform (GCP).

### Technical Checklist
- [ ] Tạo Bucket trên GCP.
- [ ] Khởi tạo Service Account trên GCP với quyền `roles/storage.objectAdmin`.
- [ ] Tải xuống tệp Service Account JSON (Credentials).
- [ ] Khởi tạo DVC và cấu hình GCP Bucket làm remote storage.
- [ ] Theo dõi tập dữ liệu với DVC và push lên GCP.

### 1. Cấu hình Google Cloud Platform (GCP)

Bạn cần thực hiện các thao tác sau trên GCP Console:
1. Tạo một GCS Bucket (ví dụ: `gs://my-mlops-dvc-bucket`).
2. Điều hướng tới IAM & Admin > Service Accounts.
3. Tạo một Service Account mới và cấp quyền **Storage Object Admin** (`roles/storage.objectAdmin`).
4. Tạo và tải xuống tệp khóa (Key) dưới dạng JSON. Lưu ý không commit tệp này lên Git.

Xuất biến môi trường (environment variable) để DVC có thể xác thực với GCP:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
```

### 2. Thiết lập DVC Remote và Theo dõi Dữ liệu

Khởi tạo DVC trong dự án và liên kết với GCS Bucket.

```bash
# Initialize DVC
dvc init

# Add GCP remote storage
# TODO: Replace with your actual GCS bucket name
dvc remote add -d myremote gs://my-mlops-dvc-bucket/dvcstore

# Track the dataset
# TODO: Ensure your dataset is inside the data/ directory
dvc add data/wine_quality.csv

# Commit DVC metadata to Git
git add data/wine_quality.csv.dvc .gitignore
git commit -m "Track dataset with DVC"

# Push data to Google Cloud Storage
dvc push
```
