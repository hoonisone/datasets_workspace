from pathlib import Path
from PPOCR.make_rec import make_ppocr_rec_dataset_from_ppocr_det_dataset


datadir = Path("W:\dataset_workspace\KAIST Scene Text Database\datasets\KAIST") # root dir path of dataset
target_datadir = Path("W:\dataset_workspace\KAIST Scene Text Database\datasets\KAIST_rec") # target root dir path of dataset
make_ppocr_rec_dataset_from_ppocr_det_dataset(datadir, target_datadir)