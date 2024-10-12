from core import OutdoorRealShotKoreanImage, OutdoorRealShotKoreanImage_To_PPOCRDet
from pathlib import Path
import json

label_file_path = Path(__file__).resolve().parent/"ppocr_dataset.txt"

dataset = OutdoorRealShotKoreanImage()
dataset = OutdoorRealShotKoreanImage_To_PPOCRDet(dataset)

print(f"Label file path = {label_file_path}")

with open(label_file_path, "w", encoding='utf-8') as f:
    for i, (x, y) in enumerate(dataset):
        path = dataset.dataset_loader.get_x_path(i)
        path = Path(path).relative_to(dataset.dataset_loader.args.dataset_dir)
        path = str(path).replace("//", "/")
        f.write(f"{path}\t{json.dumps(y, ensure_ascii=False)}\n")
