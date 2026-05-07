# 03_inference_api_and_testing.md

## API Suy luận và Kiểm thử (Inference API & Testing)

Sau khi huấn luyện mô hình, chúng ta cần triển khai mô hình dưới dạng RESTful API bằng FastAPI để phục vụ dự đoán (Inference). Ngoài ra, tài liệu này hướng dẫn thiết lập Unit Test bằng `pytest` để đảm bảo chất lượng hệ thống.

### Technical Checklist
- [ ] Xây dựng REST API bằng FastAPI (`src/serve.py`).
- [ ] Định nghĩa Pydantic schema cho Input/Output.
- [ ] Tải mô hình đã huấn luyện (được tải từ artifact hoặc thư mục cục bộ).
- [ ] Viết Unit test trong `tests/test_train.py` để kiểm thử logic.

### 1. Triển khai FastAPI (`src/serve.py`)

Hãy hoàn thành mã nguồn API suy luận.

**Tệp: `src/serve.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Wine Quality Prediction API", version="1.0.0")

# TODO: Define the Pydantic schema for Wine features
class WineInput(BaseModel):
    fixed_acidity: float
    # TODO: Add remaining 10 features for wine quality
    alcohol: float

class PredictionOutput(BaseModel):
    quality: int

# Load the trained model globally (Mock path or fetch from MLflow)
MODEL_PATH = "models/model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Model not found at {MODEL_PATH}")

@app.get("/")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
def predict(wine: WineInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")
    
    # TODO: Convert the Pydantic input to a 2D numpy array
    input_data = np.array([[]]) 
    
    # TODO: Predict using the model
    prediction = 0
    
    return {"quality": prediction}
```

### 2. Viết Unit Test (`tests/test_train.py`)

Kiểm thử xem quá trình tải dữ liệu hoặc logic khởi tạo mô hình có hoạt động đúng không.

**Tệp: `tests/test_train.py`**

```python
import pytest
import numpy as np
from src.train import load_data

def test_data_loading():
    # Mock behavior or test actual utility function
    # TODO: Write a test to ensure load_data returns correct format
    pass

def test_model_initialization():
    from sklearn.ensemble import RandomForestClassifier
    # TODO: Initialize RandomForestClassifier and test if instance is created correctly
    clf = RandomForestClassifier(n_estimators=10)
    assert clf is not None
```

Chạy kiểm thử:

```bash
pytest tests/
```
