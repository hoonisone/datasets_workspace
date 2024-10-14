from pathlib import Path
from PIL import Image
import json
from tools.polygon import crop_by_polygon
import tqdm
IGNORE_TEXT = ["(한자)", "((한자))", "(((한자)))", "(일본어)", "((일본어))", "(((일본어)))", "(외국어)","((외국어))","(((외국어)))",  "(영어)", "((영어))", "(((영어)))", "xx", "xxx", "xxxx", "xxxxx", "XX", "XXX", "XXXX", "XXXXX"]
IGNORE_MASK = ["xx", "xxx", "xxxx", "xxxxx", "XX", "XXX", "XXXX", "XXXXX"]

def text_check(text):
    # 쓸 수 있는 test(trascription) 인지 체크하여 T, F로 반환
    if text in IGNORE_TEXT: # 금지된 텍스트에 해당하면 탈락
        return False
    else:
        for mask in IGNORE_MASK: # mask를 포함하고 있으면 탈락
            if mask in text:
                return False
    return True


def get_new_image_path(i, dir_size = 1000, extension=".png"):
    # index로 부터 이미지 저장 경로 반환
    # 개수가 많아지는 것을 고려하여 일정한 개수마다 디렉터리를 구분함
    image_num = i+1
    dir_num = ((i)//dir_size)+1
    new_image_path = Path(f"{dir_num}/{image_num}").with_suffix(extension)
    return new_image_path

def make_ppocr_rec_dataset_from_ppocr_det_dataset(datadir, target_datadir):
    
    label_file = datadir/"label.txt"
    target_label_file = target_datadir/"label.txt"
    
    with open(label_file, encoding="utf-8") as f:
        lines = [line.strip().split("\t") for line in f.readlines()]

    image_paths = [line[0] for line in lines]
    labels = [json.loads(line[1]) for line in lines]
    
    if target_label_file.exists():
        target_label_file.unlink()
    
    target_label_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_label_file, "a", encoding="utf-8") as f:
        for i, (image_path, labels) in tqdm.tqdm(enumerate(zip(image_paths, labels))):
            # Image.open(datadir/image).show()
            for label in labels:
                
                if text_check(label["transcription"]):
                    polygon = label["points"]
                    image = Image.open(datadir/image_path)
                    cropped_image = crop_by_polygon(image, polygon)
                    new_label = dict(label)
                    new_label["source_image"] = image_path
                    
                    new_image_path = get_new_image_path(i)
                    (target_datadir/new_image_path).parent.mkdir(parents=True, exist_ok=True)

                    cropped_image.save(target_datadir/new_image_path)
                    f.write(f"{new_image_path}\t{json.dumps(new_label, ensure_ascii=False)}\n")

            target_datadir
            
            
