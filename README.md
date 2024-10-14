# Introduction
- Open dataset collections
- Provide fit-for-purpose preprocessing code

# Dataset
| Source        | Name                       | Size  | Utilization Domain  |Detail |
|---------------|----------------------------|------ |---------------------|-|
| AIHub         | 한국어 글자체 이미지         |       |                    |[detail](./13.%20korean%20font/README.md)|
| AIHub         | 야외 실제 촬영 한글 이미지   |       |    STR             | [detail](\OutdoorRealShotKoreanImage\README.md)  |
| IAPR-TC11     | KAIST Scene Text Database  |       | STR, STD, ...        |[detail](./KAIST%20Scene%20Text%20Database/README.md)|

# Workspace
| Source        | Name                       | Work       | Label format                              |
|---------------|----------------------------|------------|-------------------------------------------|
|               | PPOCR                       | STR, STD  | [label format](./PPOCR/label_format.md)    |

# Dataset Management Class

A deep learning dataset generally consists of samples composed of `x` (data) and `y` (label). Datasets vary in structure across different domains, so transforming datasets into the appropriate format is often necessary to apply them in any domain.

We propose an abstract dataset class to address this need.

## Dataset Class Overview

| Class     | Usage                                              |
|-----------|----------------------------------------------------|
| `Dataset` | Implemented for each specific dataset              |
| `Converter` | Implemented to transform datasets between domains |

## Example

- We have a dataset 'A' in domain (format) `α`.
- We want to transform dataset 'A' into domain `β`.
- Steps:
    1. Implement the `Dataset` class for dataset 'A'.
    2. Implement the `Converter` class to transform data from domain `α` to domain `β`.

- This approach provides high efficiency in handling combinations between datasets and domains.
