import os
import json
from PIL import Image
from pathlib import Path
from tools.dataset import Dataset_Loader, Dataset_Converter
from tools.config_loader import YamlConfigLoader

CONFIG_PATH = Path(__file__).resolve().parent/"config.yml"

class OutdoorRealShotKoreanImage_Preprocesser:
    """
        AIHUB 야외 실제 촬영 한글 이미지 데이터 셋에 대해
        폴더를 정리해주는 기능을 모은 클래스
    """
    def __init__(self, ):
        self.args = YamlConfigLoader.load_config(CONFIG_PATH)
        self.dataset_dir = self.args.dataset_dir
        self.file_path_rename_pair = self.args.file_path_rename_pair
    
    
    def unzip(self):
        ""
        origin_root = Path(self.dataset_dir) # zip 파일들이 있는 데이터 셋의 root
        target_root = Path(self.dataset_dir) # zip 파일들의 압축을 풀어 경로를 유지한 체 저장하기 시작할 대상 root
        
        for origin_path in sorted(origin_root.rglob(f"*.zip")):
            
            target_dir = target_root/origin_path.relative_to(origin_root).parent/origin_path.stem    # 파일을 저장할 디렉터리
            
            if target_dir.exists():
                print(f"Note: The target file '{target_dir}' already exist. It's not done to unzip this file. For doint this, delete the target file")
                continue
            
            target_dir.mkdir(parents=True, exist_ok=True)                                               # 유효성 체크
            
            print(f"unzip -o -O cp949 '{str(origin_path)}' -d '{str(target_dir)}'")
            os.system(f"unzip -o -O cp949 '{str(origin_path)}' -d '{str(target_dir)}'")         # 압축 해제 후 저장

    def clean_zip(self):
        for target_path in sorted(Path(self.dataset_dir).rglob(f"*.zip")):
            target_path.unlink()
            

    def get_path_pair_where_origin_exist(self):
        # pair중 origin이 root 내에 존재하는 pair만 추출하여 반환
        existing_pair = dict()
        for origin, target in self.file_path_rename_pair.items():
            origin = Path(self.dataset_dir)/origin
            if (origin).exists():
                existing_pair[origin] = target
        return existing_pair
    

    def newly_organize(self):
        # 기존의 길고 복잡한 경로를 깔끔하게 정리해줌
        # 대응되는 경로를 미리 정해져 있음
        path_pairs = self.get_path_pair_where_origin_exist() # origin이 존재하는 pair에 대해서만
                
        for origin, target in path_pairs.items():
            origin = Path(self.dataset_dir)/origin
            target = Path(self.dataset_dir)/target
            target.parent.mkdir(parents=True, exist_ok=True)
            origin.rename(target)
            print(f"'{origin}' -> '{target}'")
    

    def get_existing_target_dir(self):
        # 전체 target_dir 중 실제로 존재하는 것 만 찾아서 반환
        existing_target_dir = []
        for origin, target in self.file_path_rename_pair:
            target = Path(self.dataset_dir)/origin
            if (target).exists():
                existing_target_dir.append(target)
        return existing_target_dir # 실제로 변경 가능한 수정 사항만 담음
    

    def check_valid(self):
        # 변경된 디렉터리들이 유효한지 체크
        existing_target_list = self.get_existing_target_dir(self.dataset_dir)
        for target in existing_target_list:
            if ("source" in target) and (target.replace("source", "label") not in existing_target_list):
                label_dir = target.replace("source", "label") 
                print(f"The image dir '{target}' needs label dir '{label_dir}'")
                assert False, "Not Invalid Dataset"

    def clean_origin_dir(self):
        dir_list = ["030.야외 실제 촬영 한글 이미지", "야외 실제 촬영 한글 이미지"]
        
        for dir in dir_list:
            dir = Path(self.dataset_dir)
            if dir.exists():
                dir.unlink()
    
    def preprocess(self): 
        n = 5
        print(f"(1/{n}) root 내에 모든 zip 파일 압축 해제")#######################################################
        self.unzip() # root 내에 모든 zip 파일 압축 해제
        
        print(f"(2/{n}) 남아있는 모든 zip 파일 제거")#######################################################
        # self.clean_zip() # 남아있는 모든 zip 파일 제거
        # 1번이 정상 작동 한 경우에만 실행할 것
        
        print(f"(3/{n}) 새롭게 디렉터리 구조화 (경로 정리)")#######################################################
        self.newly_organize() # 새롭게 디렉터리 구조화 (경로 정리)
        
        print(f"(4/{n}) 이미지와 레이블이 잘 대응되어 존재하는지 점검")#######################################################
        self.check_valid() # 이미지와 레이블이 잘 대응되어 존재하는지 점검
        
        print(f"(5/{n}) 불필요한 기존 폴더 제거 (빈 폴더 제거)")#######################################################
        self.clean_origin_dir() # 불필요한 기존 폴더 제거 (빈 폴더 제거)

class OutdoorRealShotKoreanImage(Dataset_Loader):
    """
        야외 실제 촬영 한글 이미지 데이터 셋에 대한 데이터 셋 객체
        데이터를 직접 다운해야 함
    """
    
    @staticmethod
    def __get_checked_dir_list(checklist, path):
        # 전체 데이터 중 어떤 데이터는 쓰고 어떤건 안쓸지 결정
        path = Path(path)
        if isinstance(checklist, dict):
            if checklist["all"] == True:
                return [path]
            elif checklist["all"] == False:
                return []
            else:
                del checklist["all"]
                return sum([OutdoorRealShotKoreanImage.__get_checked_dir_list(v, path/k) for k, v in checklist.items()], [])

        if checklist == True:
            return [path]
        else:
            return []

    def get_x(self, index):
        return self.__load_x(self.get_x_path(index))
    
    def get_y(self, index):
        return self.__load_y(self.get_y_path(index))
    
    def _show_x(self, x):
        x.show()
        
    def _show_y(self, y):
        print(y)
        
    def _show_x_y(self, y):
        pass    
    

    
        
    def __len__(self):
        return len(self.sample_list)
    
    def __init__(self):
        self.args = YamlConfigLoader.load_config(CONFIG_PATH)
        
        checklist = self.args.checklist
        self.dataset_dir = self.args.dataset_dir
        

        self.checked_dir_list = self.get_checked_dir_list(checklist)
        
        print("*******Checked Dir List*******")
        for dir in self.checked_dir_list:
            print(dir)
        print("******************************")
        self.sample_list = self.__get_all_sample_list()
        super().__init__()

    def get_checked_dir_list(self, checklist_dir_list):
        checked_dir_list = OutdoorRealShotKoreanImage.__get_checked_dir_list(checklist_dir_list, "")
        return [Path(self.dataset_dir)/x for x in checked_dir_list]
    
    def get_x_path(self, index):
        return self.sample_list[index][0]
    
    def get_y_path(self, index):
        return self.sample_list[index][1]
    

    
    def __load_x(self, path):
        return Image.open(path)
    
    def __load_y(self, path):
        with open(path, encoding='utf-8') as f:
            return json.load(f)
        
    def __get_all_sample_list(self):
        img_ext = self.args.x_ext
        label_ext = self.args.y_ext
        sample_list = []
                
        for checked_dir in self.checked_dir_list:
            for img_path in sorted(Path(checked_dir).rglob(f"*.{img_ext}")):
                label_path = img_path.parent/f"{img_path.stem}.{label_ext}"
                label_path = Path(str(label_path).replace("source", "label"))
                sample_list.append([img_path, label_path])
        return sample_list
    
    
class OutdoorRealShotKoreanImage_To_PPOCRDet(Dataset_Converter):
    def transform_x(self, x):
        return x
    
    def transform_y(self, y):
        label = y
        result = []
        for annotation in label["annotations"]:
            try:
                
                x, y, w, h = annotation["bbox"]
                upper_left = [x, y]
                upper_right = [x+w, y]
                bottom_right = [x+w, y+h]
                bottom_left = [x, y+h]
            except:
                continue
            result.append({"transcription":annotation["text"], "points":[upper_left, upper_right, bottom_right, bottom_left]})
        return result    
    
    
    
    
if __name__ == "__main__":
    dataset = OutdoorRealShotKoreanImage()
    # dataset.show_x(2)
    dataset.show_y(2)

    dataset = OutdoorRealShotKoreanImage_To_PPOCRDet(dataset)
    # dataset.show_x(2)
    dataset.show_y(2)