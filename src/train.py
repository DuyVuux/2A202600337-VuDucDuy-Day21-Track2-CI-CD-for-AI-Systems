import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# Cau hinh logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

EVAL_THRESHOLD = 0.70

def check_data_drift(df: pd.DataFrame, target_col: str = "target"):
    """
    Bonus 5: Kiem tra phan phoi nhan de canh bao Data Drift.
    Canh bao neu bat ky class nao co ty le < 10%.
    """
    counts = df[target_col].value_counts(normalize=True)
    logger.info(f"Phan phoi nhan:\n{counts}")
    
    drift_detected = False
    for label, proportion in counts.items():
        if proportion < 0.10:
            logger.warning(f"CANH BAO: Lop '{label}' chi chiem {proportion:.2%}, duoi nguong 10%!")
            drift_detected = True
    
    if not drift_detected:
        logger.info("Khong phat hien bat thuong ve phan phoi nhan.")

def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.
    """
    logger.info(f"Bat dau huan luyen voi du lieu: {data_path}")

    # Step 1: Doc du lieu
    if not os.path.exists(data_path) or not os.path.exists(eval_path):
        logger.error("Khong tim thay file du lieu!")
        raise FileNotFoundError("Data path or eval path does not exist.")

    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    # Bonus 5: Check Data Drift truoc khi train
    check_data_drift(df_train)

    # Step 2: Tach dac trung va nhan
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    # Cau hinh MLflow tu bien moi truong (bao mat)
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        logger.info(f"MLflow Tracking URI: {tracking_uri}")

    with mlflow.start_run():
        # Step 3: Ghi nhan tham so
        mlflow.log_params(params)
        logger.info(f"Logged params: {params}")

        # Step 4: Huan luyen RandomForest
        model = RandomForestClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        # Step 5: Du doan va tinh chi so
        preds = model.predict(X_eval)
        acc = accuracy_score(y_eval, preds)
        f1 = f1_score(y_eval, preds, average="weighted")

        # Step 6: Ghi nhan metrics vao MLflow
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        # Step 7: In ket qua
        logger.info(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # Step 8: Luu metrics ra file outputs/metrics.json
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/metrics.json", "w") as f:
            json.dump({"accuracy": acc, "f1_score": f1}, f)
        logger.info("Da luu metrics vao outputs/metrics.json")

        # Step 9: Luu mo hinh ra file models/model.pkl
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")
        logger.info("Da luu model vao models/model.pkl")

    return acc

if __name__ == "__main__":
    try:
        with open("params.yaml") as f:
            params = yaml.safe_load(f)
        train(params)
    except Exception as e:
        logger.exception(f"Loi trong qua trinh huan luyen: {e}")
        exit(1)
