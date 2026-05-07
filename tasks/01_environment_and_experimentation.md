# 01_environment_and_experimentation.md

## Thiết lập Môi trường và Theo dõi Thử nghiệm (Environment & Experimentation)

Tài liệu này hướng dẫn cách thiết lập môi trường phát triển cục bộ (local development environment), quản lý các biến môi trường và tích hợp MLflow vào mã nguồn huấn luyện mô hình để theo dõi các siêu tham số (hyperparameters) và các chỉ số đo lường (metrics).

### Technical Checklist
- [ ] Khởi tạo môi trường ảo Python (Virtual Environment) và cài đặt các thư viện cần thiết.
- [ ] Thiết lập tệp `.env` cho MLflow.
- [ ] Cấu trúc tệp `params.yaml` chứa siêu tham số.
- [ ] Tích hợp MLflow vào tệp `src/train.py` để log metrics, parameters và model.

### 1. Thiết lập Môi trường Cục bộ

Đầu tiên, tạo môi trường ảo và cài đặt các dependencies từ `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Tạo tệp `.env` ở thư mục gốc để chứa cấu hình MLflow tracking URI (sử dụng DagsHub hoặc máy chủ MLflow nội bộ):

```env
MLFLOW_TRACKING_URI=https://dagshub.com/DuyVuux/2A202600337-VuDucDuy-Day21-Track2-CI-CD-for-AI-Systems.mlflow
MLFLOW_TRACKING_USERNAME=your-username
MLFLOW_TRACKING_PASSWORD=your-token
```

### 2. Tích hợp MLflow vào `src/train.py`

Chúng ta cần hoàn thiện mã nguồn huấn luyện mô hình Random Forest dự đoán chất lượng rượu (Wine Quality). Hãy điền vào các phần `TODO`.

**Tệp: `src/train.py`**

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import yaml
import mlflow
import mlflow.sklearn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_data(data_path):
    # TODO: Load dataset from data_path
    pass

def train():
    # Load configurations
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    
    n_estimators = params["train"]["n_estimators"]
    max_depth = params["train"]["max_depth"]
    
    # Load and split data
    df = load_data("data/wine_quality.csv")
    # TODO: Split df into train and test sets (X_train, X_test, y_train, y_test)
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    mlflow.set_experiment("wine-quality-experiment")

    with mlflow.start_run():
        # TODO: Initialize RandomForestClassifier with n_estimators and max_depth
        
        # TODO: Fit the model
        
        # TODO: Make predictions and calculate accuracy
        
        # MLflow Tracking
        # TODO: Log parameters (n_estimators, max_depth) using mlflow.log_param
        # TODO: Log metrics (accuracy) using mlflow.log_metric
        # TODO: Log the trained model using mlflow.sklearn.log_model

if __name__ == "__main__":
    train()
```
