# 04_cicd_pipeline_engineering.md

## Kỹ thuật Đường ống CI/CD (CI/CD Pipeline Engineering)

Tài liệu này hướng dẫn xây dựng luồng tự động hóa bằng GitHub Actions. Đường ống (Pipeline) sẽ bao gồm các công việc (jobs) Kiểm thử, Huấn luyện, Đánh giá và Triển khai.

### Technical Checklist
- [ ] Khởi tạo tệp `.github/workflows/mlops.yml`.
- [ ] Thiết lập Job: `test` (chạy `pytest`).
- [ ] Thiết lập Job: `train_and_eval` (Kéo dữ liệu từ DVC, chạy `src/train.py`).
- [ ] Định nghĩa logic kiểm tra độ chính xác (Accuracy >= 0.70).
- [ ] Thiết lập Job: `deploy` (Kết nối SSH tới máy chủ đích và khởi động lại FastAPI).

### 1. Cấu hình GitHub Actions Workflow

Tạo thư mục `.github/workflows/` và bổ sung tệp `mlops.yml`.

**Tệp: `.github/workflows/mlops.yml`**

```yaml
name: MLOps CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Pytest
        run: |
          # TODO: Execute pytest
          pytest tests/

  train_and_eval:
    needs: test
    runs-on: ubuntu-latest
    env:
      GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_CREDENTIALS }}
      MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Pull data with DVC
        run: |
          # TODO: Configure GCP Credentials for DVC
          dvc pull
          
      - name: Train Model
        run: |
          # TODO: Run the training script
          python src/train.py
          
      - name: Evaluate Model Performance
        run: |
          # TODO: Write a small script to parse accuracy and fail if < 0.70
          echo "Checking if accuracy meets the threshold >= 0.70..."

  deploy:
    needs: train_and_eval
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            # TODO: Commands to pull latest code and restart FastAPI
            cd /path/to/project
            git pull origin main
            source .venv/bin/activate
            pip install -r requirements.txt
            # Restart systemctl or uvicorn
            # systemctl restart fastapi-wine
```

Lưu ý: Bạn phải thêm các `secrets` (`GCP_CREDENTIALS`, `MLFLOW_TRACKING_URI`, `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`) vào Repository Settings > Secrets and variables > Actions.
