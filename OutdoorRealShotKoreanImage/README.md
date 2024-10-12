# Source
[AIHub](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=105)

# How to use

### 1. Data download
- **Download following datasets in [AIHub](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=105)**
  1. **030. 야외 실제 촬영 한글 이미지**
  2. **야외 실제 촬영 한글 이미지**

### 2. Preprocessing

#### 1) Set right data dir path in config
- In `./preprocess/config.yml` set the data dir path as value of `dataset_dir`
  ```
    dataset_dir: /home/datasets
  ```

- dataset_dir는 아래와 같은 구조여야 한다.
  ```
  dataset_dir
  ├── 030. 야외 실제 촬영 한글 이미지
  └── 야외 실제 촬영 한글 이미지
  ```



#### 2) Preprocessing
- The datasets has some complicated form
- So, There's need to re-organize
```bash
python preprocess/preprocess.py
# Preprocessing
# (1) unzip      !!! It doesn't work on windows (you can unzip using zip program directly)
# (2) remove zip files
# (3) make dir clean by re-organizing and chaning path name short
# (4) validate pair of data and label
# (5) clean the unnecessary dir and files
```

<details>
<summary>After dir re-organizing</summary>

  ```
  dataset_dir
  ├── train1
  │   ├── label
  │   └── source
  ├── train2
  │   ├── label
  │   └── source
  ├── val1
  │   ├── label
  │   └── source
  └── val2
      ├── label
      └── source
  ```
</details>

### 3. Setting of Data Usage Range
- **AIhub Outdoor Real Shot Korean Image Dataset** contains images from various domains.
- You can select specific domains to include in your data usage.
- Modify `setting` elements in the file `OutdoorRealShotKoreanImage/config/main_config.yml`.
- If you want to use all data, just put `true` as the value of element `all`.
  ```yaml
    checklist:
      all: true
  ```

<details>
<summary>Key-Value meaning</summary>

| Key (Catogory) | Value (Usage)  | Meaning                            |
|----------------|----------------|------------------------------------|
| `all`          | true           | Use all subcategories.             |
| `all`          | false          | Do not use any subcategories.      |
| `all`          | null           | Select subcategories manually.     |
| `category`     | null           | Use specific subcategories.        |
</details>

<details>
  <summary>Example Configuration</summary>

  ```yaml
  checklist:
    all: null
    A:
      all: null
      A_1:
        all: false
        A_1_1: true
        A_1_2: true
      A_2:
        all: true
        A_2_1: false
        A_2_2: true
    B:
      B_1:
        all: null
        B_1_1: true
        B_1_2: false
      B_2:
        all: true
        B_2_1: true
        B_2_2: false
  ```
  
  #### category selection result:
  | Key   | Usage  |    1     |     2       |      3        |
  |-------|--------|----------|-------------|---------------|
  | A_1_1 | false  | A (Null) | A_1 (Fasle) |               |
  | A_1_2 | false  | A (Null) | A_1 (Fasle) |               |
  | A_2_1 | true   | A (Null) | A_2 (True)  |               |
  | A_2_2 | true   | A (Null) | A_2 (True)  |               |
  | B_1_1 | true   | B (Null) | B_1 (Null)  | B_1_1 (True)  |
  | B_1_2 | false  | B (Null) | B_1 (Null)  | B_1_2 (False) |
  | B_2_2 | true   | B (Null) | B_1 (Null)  | B_2_1 (True)  |
  | B_2_2 | false  | B (Null) | B_1 (Null)  | B_2_2 (False) |
</details>


### 4. Make ppocr det dataset
- run following code
``` bash
  python ./OutdoorRealShotKoreanImage/make_ppocr_det.py
```
- the dataset set is now PPOCR det dataset

### 5. Make ppocr rec dataset
- put the right dataset dir path in python code `make_ppocr_det.py`
- run following code
``` bash
  python ./OutdoorRealShotKoreanImage/make_ppocr_rec.py
```
- the target dataset is now PPOCR rec dataset