import pandas as pd
import os
import logging

# Cau hinh logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TRAIN_DATA_PATH = "data/train_phase1.csv"
NEW_DATA_PATH = "data/train_phase2.csv"

def add_new_data():
    """
    Gop du lieu moi tu train_phase2.csv vao train_phase1.csv.
    Day la buoc chuan bi cho viec huan luyen lai model (Continuous Training).
    """
    # 1. Kiem tra su ton tai cua cac file
    if not os.path.exists(TRAIN_DATA_PATH):
        logger.error(f"Khong tim thay file du lieu goc: {TRAIN_DATA_PATH}")
        return
    
    if not os.path.exists(NEW_DATA_PATH):
        logger.warning(f"Khong tim thay du lieu moi tai {NEW_DATA_PATH}. Bo qua.")
        return

    try:
        # 2. Doc du lieu
        df_original = pd.read_csv(TRAIN_DATA_PATH)
        df_new = pd.read_csv(NEW_DATA_PATH)
        
        original_size = len(df_original)
        new_size = len(df_new)
        
        logger.info(f"Dang gop {new_size} mau moi vao tap du lieu goc ({original_size} mau)...")

        # 3. Gop du lieu
        df_updated = pd.concat([df_original, df_new], ignore_index=True)
        
        # Loai bo trung lap neu can (tuy chon)
        # df_updated = df_updated.drop_duplicates()

        # 4. Luu lai file goc (de DVC track su thay doi)
        df_updated.to_csv(TRAIN_DATA_PATH, index=False)
        
        logger.info(f"Cap nhat thanh cong! Kich thuoc moi: {len(df_updated)} mau.")
        
    except Exception as e:
        logger.error(f"Loi khi gop du lieu: {e}")
        raise

if __name__ == "__main__":
    add_new_data()
