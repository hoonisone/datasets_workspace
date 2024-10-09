# Source
[KAIST Scene Text Database](http://www.iapr-tc11.org/mediawiki/index.php/KAIST_Scene_Text_Database)
- **Version**: 1.0
- **Created**: 2011-01-11
- **Last updated**: 2012-10-17


---------------------------------------------------------------------------------------------------------------------------------
# Version 1.0
original version from the official website

### Statistics
| State                   | Description                         | Correction                        | Num   |
|-------------------------|-------------------------------------|-----------------------------------|------:|
| NO_ERROR                | Normal data                         |                                   |  2364 |
| PARSING_ERROR           | just format error                   | correct format                    |     5 |
| FORMAT_ERROR            | just format error                   | correct format                    |     2 |
| PARTIALLY_NO_CHARACTER  | one more words have no character    | only use the words with character |    47 |
| NO_CHARACTER            | all words have no character         | remove completely                 |    28 |



<details>
  <summary>Error sample detail</summary>

  | File Path                                                  | State                  | Correction detail                        |
  |------------------------------------------------------------|------------------------|------------------------------------------|
  | /KAIST/English/Digital_Camera/(E.S)C-outdoor1/080116-0065  | PARSING_ERROR          | remove `</image>` tag in line 3          |
  | /KAIST/English/Digital_Camera/(E.S)F-others/4              | PARSING_ERROR          | 이유는 모르겠으나 첫번째 줄에서 오류나서 1번 줄 지움 |
  | /KAIST/Korean/Digital_Camera/E-night/3                     | PARSING_ERROR          | 끝에 `</image>` `</images>` 태그 2개 누락   |
  | /KAIST/Korean/Digital_Camera/G-others/080116-0079          | PARSING_ERROR          | 앞에 인덴테이션 문자 제거 및 끝에 `</images>` 태그 추가 |
  | /KAIST/Korean/Digital_Camera/indoor1/080119-0001           | PARSING_ERROR          | 끝에 `</image>` 태그 2개 중복           |
  | /KAIST/English/Digital_Camera/(E.S)C-outdoor1/080116-0055  | FORMAT_ERROR           | 맨 바깥에 `<images>` 태그 누락 됌        |
  | /KAIST/English/Digital_Camera/(E.S)C-outdoor1/080116-0089  | FORMAT_ERROR           | 맨 바깥에 `<images>` 태그 누락           |
  | /KAIST/English/Digital_Camera/(E.S)C-outdoor2/P1010026     | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Digital_Camera/(E.S)D-indoor/DSC02861       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Digital_Camera/(E.S)D-indoor/DSC03086       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Digital_Camera/(E.S)D-indoor/DSC03143       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Digital_Camera/(E.S)D-indoor/DSC03946       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Mobile_Phone/(E.M)A-outdoor/P090912050      | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Mobile_Phone/(E.M)B-indoor/P090911050       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/English/Mobile_Phone/(E.M)C-bookCover/P090905003    | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/F-bookCover/DSC02828          | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/G-others/DSC02668             | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/indoor1/DSC02730              | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/outdoor3/DSC02921             | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/outdoor5/DSC03748             | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Digital_Camera/outdoor7/P1010036             | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)A-shadow/P090912051        | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)C-outdoor/P090912060       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)C-outdoor/P090912076       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)E-bookCover/P090905001     | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)E-bookCover/P090911048     | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Korean/Mobile_Phone/(M,K)E-bookCover/P090912011     | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Digital_Camera/(C.S)C-outdoor2/DSC02920       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Digital_Camera/(C.S)C-outdoor3/DSC02963.xml   | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Digital_Camera/(C.S)C-outdoor4/DSC03747       | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Digital_Camera/(C.S)D-indoor1/DSC02763        | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Digital_Camera/(C.S)D-indoor1/DSC02795        | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Mobile_Phone/(C.M)A-outdoor/P090912054        | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Mobile_Phone/(C.M)A-outdoor/P090912057        | PARTIALLY_NO_CHARACTER |                                          |
  | /KAIST/Mixed/Mobile_Phone/(C.M)A-outdoor/P090912071        | PARTIALLY_NO_CHARACTER |                                          |

</details>

# Version 1.1
* correct label format and remove unusable label
### Statistics
| State                   | Description                         | Correction                        | Num   |
|-------------------------|-------------------------------------|-----------------------------------|------:|
| NO_ERROR                | Normal data                         |                                   |  2471 |
| PARSING_ERROR           | just format error                   | correct format                    |     0 |
| FORMAT_ERROR            | just format error                   | correct format                    |     0 |
| PARTIALLY_NO_CHARACTER  | one more words have no character    | only use the words with character |    47 |
| NO_CHARACTER            | all words have no character         | remove completely                 |     0 |