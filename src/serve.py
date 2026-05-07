from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from google.cloud import storage
import joblib
import os
import logging
import time

# Cau hinh logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Wine Quality Prediction API")

GCS_BUCKET = os.environ.get("GCS_BUCKET")
GCS_MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = os.path.expanduser("~/models/model.pkl")

# Mapping label
LABEL_MAPPING = {0: "thap", 1: "trung_binh", 2: "cao"}

def download_model():
    """
    Tai file model.pkl tu GCS ve may khi server khoi dong.
    """
    if not GCS_BUCKET:
        logger.warning("GCS_BUCKET khong duoc thiet lap. Bo qua viec tai model tu GCS.")
        return

    try:
        logger.info(f"Dang tai model tu gs://{GCS_BUCKET}/{GCS_MODEL_KEY}...")
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        blob = bucket.blob(GCS_MODEL_KEY)
        
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        blob.download_to_filename(MODEL_PATH)
        logger.info(f"Model da duoc tai xuong thanh cong tai {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Loi khi tai model tu GCS: {e}")

# Khoi tao model
model = None
download_model()
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("Model da duoc load thanh cong vao bo nho.")
    except Exception as e:
        logger.error(f"Loi khi load model file: {e}")
else:
    logger.error(f"Model file khong ton tai tai {MODEL_PATH}")

class PredictRequest(BaseModel):
    features: list[float]

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration:.4f}s")
    return response

@app.get("/health")
def health():
    """
    Endpoint kiem tra suc khoe server.
    """
    if model is None:
        return {"status": "unhealthy", "reason": "Model not loaded"}
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    """
    Endpoint suy luan chinh.
    """
    # Step 1: Kiem tra model
    if model is None:
        logger.error("Yeu cau predict nhung model chua duoc load.")
        raise HTTPException(status_code=500, detail="Model is not available on the server.")

    # Step 2: Kiem tra so luong dac trung
    if len(req.features) != 12:
        logger.warning(f"Dau vao sai so luong dac trung: {len(req.features)} (ky vong 12)")
        raise HTTPException(
            status_code=400, 
            detail=f"Expected 12 features, but got {len(req.features)}."
        )

    try:
        # Step 3: Du doan
        prediction = int(model.predict([req.features])[0])
        label = LABEL_MAPPING.get(prediction, "unknown")
        
        logger.info(f"Prediction success: {prediction} ({label})")
        
        # Step 4: Tra ve ket qua
        return {
            "prediction": prediction,
            "label": label
        }
    except Exception as e:
        logger.error(f"Loi trong qua trinh suy luan: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
