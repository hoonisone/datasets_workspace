import tqdm
import json
import shutil
from pathlib import Path
from enum import Enum, auto
import xml.etree.ElementTree as ET

origin_new_pair = {
    'English/Digital_Camera/(E.S)C-outdoor1/080116-0065.xml'    :"1.xml",
    'English/Digital_Camera/(E.S)F-others/4.xml'                :"2.xml",
    'Korean/Digital_Camera/E-night/3.xml'                       :"3.xml",
    'Korean/Digital_Camera/G-others/080116-0079.xml'            :"4.xml",
    'Korean/Digital_Camera/indoor1/080119-0001.xml'             :"5.xml",
    'English/Digital_Camera/(E.S)C-outdoor1/080116-0055.xml'    :"6.xml",
    'English/Digital_Camera/(E.S)C-outdoor1/080116-0089.xml'    :"7.xml"
}

remove_files = [
 "English/Digital_Camera/(E.S)C-outdoor2/P1010026.xml",
 "English/Digital_Camera/(E.S)D-indoor/DSC02861.xml",
 "English/Digital_Camera/(E.S)D-indoor/DSC03086.xml",
 "English/Digital_Camera/(E.S)D-indoor/DSC03143.xml",
 "English/Digital_Camera/(E.S)D-indoor/DSC03946.xml",
 "English/Mobile_Phone/(E.M)A-outdoor/P090912050.xml",
 "English/Mobile_Phone/(E.M)B-indoor/P090911050.xml",
 "English/Mobile_Phone/(E.M)C-bookCover/P090905003.xml",
 "Korean/Digital_Camera/F-bookCover/DSC02828.xml",
 "Korean/Digital_Camera/G-others/DSC02668.xml",
 "Korean/Digital_Camera/indoor1/DSC02730.xml",
 "Korean/Digital_Camera/outdoor3/DSC02921.xml",
 "Korean/Digital_Camera/outdoor5/DSC03748.xml",
 "Korean/Digital_Camera/outdoor7/P1010036.xml",
 "Korean/Mobile_Phone/(M,K)A-shadow/P090912051.xml",
 "Korean/Mobile_Phone/(M,K)C-outdoor/P090912060.xml",
 "Korean/Mobile_Phone/(M,K)C-outdoor/P090912076.xml",
 "Korean/Mobile_Phone/(M,K)E-bookCover/P090905001.xml",
 "Korean/Mobile_Phone/(M,K)E-bookCover/P090911048.xml",
 "Korean/Mobile_Phone/(M,K)E-bookCover/P090912011.xml",
 "Mixed/Digital_Camera/(C.S)C-outdoor2/DSC02920.xml",
 "Mixed/Digital_Camera/(C.S)C-outdoor3/DSC02963.xml",
 "Mixed/Digital_Camera/(C.S)C-outdoor4/DSC03747.xml",
 "Mixed/Digital_Camera/(C.S)D-indoor1/DSC02763.xml",
 "Mixed/Digital_Camera/(C.S)D-indoor1/DSC02795.xml",
 "Mixed/Mobile_Phone/(C.M)A-outdoor/P090912054.xml",
 "Mixed/Mobile_Phone/(C.M)A-outdoor/P090912057.xml",
 "Mixed/Mobile_Phone/(C.M)A-outdoor/P090912071.xml"
]   


def xml_to_dict(element):
    # 요소의 속성을 dict로 변환
    node = {}
    if element.attrib:
        node['@attributes'] = element.attrib
    
    # 요소의 텍스트가 있으면 추가
    if element.text and element.text.strip():
        node['#text'] = element.text.strip()
    
    # 자식 요소 처리
    for child in element:
        child_dict = xml_to_dict(child)
        if child.tag not in node:
            node[child.tag] = child_dict
        else:
            if isinstance(node[child.tag], list):
                node[child.tag].append(child_dict)
            else:
                node[child.tag] = [node[child.tag], child_dict]
    
    return node

def xml_file_to_json(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    xml_dict = xml_to_dict(root)
    return xml_dict



class XML_STATE(Enum):
    NO_ERROR = auto()
    PARSING_ERROR = auto()
    FORMAT_ERROR = auto()
    PARTIALLY_NO_CHARACTER = auto()
    NO_CHARACTER = auto()

def check_xml_structure(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # 루트 태그가 <images>인지 확인
        if root.tag != 'images':
            return XML_STATE.FORMAT_ERROR

        # <image> 태그가 존재하는지 확인
        for image in root.findall('image'):
            # <imageName> 태그가 존재하는지 확인
            if image.find('imageName') is None:
                return XML_STATE.FORMAT_ERROR
            
            # <resolution> 태그와 속성 "x", "y"가 있는지 확인
            resolution = image.find('resolution')
            if resolution is None or 'x' not in resolution.attrib or 'y' not in resolution.attrib:
                return XML_STATE.FORMAT_ERROR

            # <words> 태그 및 그 하위 <word> 태그 확인
            words = image.find('words')
            if words is None:
                return XML_STATE.FORMAT_ERROR


            total_character_num = 0
            partially_no_character_flag = False
            for word in words.findall('word'):
                # <word> 태그에 속성 "x", "y", "width", "height"가 있는지 확인
                if 'x' not in word.attrib or 'y' not in word.attrib or 'width' not in word.attrib or 'height' not in word.attrib:
                    return XML_STATE.FORMAT_ERROR

                # <character> 태그가 하나도 없는 경우 체크
                characters = word.findall('character')
                total_character_num += len(characters)
                if len(characters) == 0:
                    partially_no_character_flag = True

                    # print(f"Warning: <word> 태그 내에 <character>가 없습니다. (word: {word.attrib})")
                
                # <character> 태그가 있을 경우, 속성 확인
                for char in characters:
                    if 'x' not in char.attrib or 'y' not in char.attrib or 'width' not in char.attrib or 'height' not in char.attrib or 'char' not in char.attrib:
                        return XML_STATE.FORMAT_ERROR
                    
            if total_character_num == 0:
                return XML_STATE.NO_CHARACTER

            # <illumination> 태그가 있는지 확인
            if image.find('illumination') is None:
                return XML_STATE.FORMAT_ERROR

            # <difficulty> 태그가 있는지 확인
            if image.find('difficulty') is None:
                return XML_STATE.FORMAT_ERROR

            # <tag> 태그가 있는지 확인
            if image.find('tag') is None:
                return "format error"

        # 모든 체크를 통과하면 True 반환
        if partially_no_character_flag:
            return XML_STATE.PARTIALLY_NO_CHARACTER
        else:
            return XML_STATE.NO_ERROR

    except ET.ParseError:
        return XML_STATE.PARSING_ERROR
    
    
    



def inspect_label(dataset_dir = Path("datasets/KAIST"), print_report=True, return_report=False, tqdm_disable = True):
    ### collect all xml file
    file_path_list = dataset_dir.glob("**/*.xml")

    ### inspect xml state
    inspect_report = {x:[] for x in XML_STATE}
    for file_path in tqdm.tqdm(file_path_list, disable = tqdm_disable):
        result = check_xml_structure(file_path)
        inspect_report[result].append(file_path)
        
    if print_report:
        for k, v in inspect_report.items():
            print(k, len(v))
    
    if return_report:
        return inspect_report




def correct_label(origin_data_dir = Path("./datasets/KAIST"), corrected_data_dir = Path("./datasets/corrected_label_files")):
    # origin file을 corrected file로 덮어 씌우기 
    for origin, new in origin_new_pair.items():
        shutil.copy2(corrected_data_dir/new, origin_data_dir/origin)    
        
        
def remove_unusable_files(origin_data_dir = Path("./datasets/KAIST")):
    remove_file_num = 0
    for file in remove_files:
        file = (origin_data_dir/file)
        if file.exists():
            remove_file_num += 1
            file.unlink()
            
    print(f"{remove_file_num} files were removed!!!")
    
    
    


def transform_label_into_ppocr_rec_form(xml_file):
    try:
        x = xml_file_to_json(xml_file)
        # print(x)
        
        words = x["image"]["words"]["word"]

        label = list()
        if isinstance(words, dict):
            words = [words]
            
            
        for word in words:
            word_range = word["@attributes"]
            x, y, w, h = int(word_range["x"]), int(word_range["y"]), int(word_range["width"]), int(word_range["height"])
            word_range = [[x, y], [x+w, y], [x+w, y+h], [x, y+h]]
            
            if "character" not in word:
                continue
            if isinstance(word["character"], dict):
                continue 

            characters = "".join([c["@attributes"]["char"] for c in word["character"]])
            label.append({"transcription": characters, "points": word_range})
        return label
    except Exception as e:
        print(xml_file, e)
        return None


def make_pporc_det_label(dataset_dir = Path("datasets/KAIST"), label_file_path = Path("./datasets/KAIST/label.txt"), extension="png"):
    inspect_report = inspect_label(dataset_dir = dataset_dir, print_report=False, return_report=True)
    file_path_list = inspect_report[XML_STATE.NO_ERROR] + inspect_report[XML_STATE.PARTIALLY_NO_CHARACTER]
    
    if label_file_path.exists():
        label_file_path.unlink()    

    with open(label_file_path, "a") as f:
        for file_path in file_path_list:
            label = transform_label_into_ppocr_rec_form(file_path)
            file_path = str(file_path.relative_to(dataset_dir).with_suffix(extension)).replace("\\", "/")
            label = json.dumps(label, ensure_ascii=False)
            f.write(f"{file_path}\t{label}\n")
    
    print(f"label file has been made for {len(file_path_list)} samples in '{label_file_path}'")