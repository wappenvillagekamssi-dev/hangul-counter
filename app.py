import streamlit as st
from collections import defaultdict
import string

# =====================
# 한글 분해 테이블
# =====================
CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
JUNG = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
JONG = ["", "ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

# =====================
# 쌍자음 분해 규칙
# =====================
double_consonant_map = {
    "ㄲ": "ㄱ",
    "ㄸ": "ㄷ",
    "ㅃ": "ㅂ",
    "ㅆ": "ㅅ",
    "ㅉ": "ㅈ"
}

# =====================
# 모음 분해 규칙 (감씨 기준)
# =====================
vowel_map = {
    "ㅏ": ["ㅏ"],
    "ㅑ": ["ㅑ"],
    "ㅐ": ["ㅐ"],
    "ㅔ": ["ㅔ"],
    "ㅖ": ["ㅖ"],
    "ㅣ": ["ㅣ"],
    "ㅓ": ["ㅏ"],
    "ㅕ": ["ㅑ"],
    "ㅗ": ["ㅏ"],
    "ㅛ": ["ㅑ"],
    "ㅜ": ["ㅏ"],
    "ㅠ": ["ㅑ"],
    "ㅡ": ["ㅣ"],
    "ㅚ": ["ㅏ", "ㅣ"],
    "ㅟ": ["ㅏ", "ㅣ"],
    "ㅘ": ["ㅏ", "ㅏ"],
    "ㅙ": ["ㅏ", "ㅐ"],
    "ㅝ": ["ㅏ", "ㅏ"],
    "ㅞ": ["ㅏ", "ㅔ"],
    "ㅢ": ["ㅣ", "ㅣ"]
}

# =====================
# 한글 개수 세기
# =====================
def count_korean(text):
    count = defaultdict(int)

    for ch in text:
        if not ("가" <= ch <= "힣"):
            continue

        idx = ord(ch) - 0xAC00

        # ---- 초성 ----
        cho = CHO[idx // 588]
        if cho in double_consonant_map:
            base = double_consonant_map[cho]
            count[base] += 2
        else:
            count[cho] += 1

        # ---- 중성 ----
        jung = JUNG[(idx % 588) // 28]
        for v in vowel_map[jung]:
            count[v] += 1

        # ---- 종성 ----
        jong = JONG[idx % 28]
        if jong:
            if jong in double_consonant_map:
                base = double_consonant_map[jong]
                count[base] += 2
            else:
                count[jong] += 1

    return dict(count)

# =====================
# 영어 알파벳 개수 세기
# =====================
def count_english(text):
    count = defaultdict(int)

    for ch in text.upper():
        if ch in string.ascii_uppercase:
            count[ch] += 1

    return dict(count)

# =====================
# Streamlit UI
# =====================
st.title("한글 · 영어 글자 개수 계산기")
st.write(
    "한글과 영어를 입력하면 "
    "자음·모음(분해 기준) 및 알파벳 개수를 자동으로 계산합니다."
)

text = st.text_input("문구를 입력하세요")

if text:
    st.subheader("🔸 한글 결과")
    kr_result = count_korean(text)
    if kr_result:
        for k, v in sorted(kr_result.items()):
            st.write(f"{k} : {v}")
    else:
        st.write("한글이 없습니다.")

    st.subheader("🔸 영어 결과")
    en_result = count_english(text)
    if en_result:
        for k, v in sorted(en_result.items()):
            st.write(f"{k} : {v}")
    else:
        st.write("영어 알파벳이 없습니다.")
