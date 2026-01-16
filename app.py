import streamlit as st
from collections import Counter

# ===============================
# 한글 분해용 데이터
# ===============================

CHOSUNG = [
    "ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ",
    "ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"
]

JUNGSUNG = [
    "ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ",
    "ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"
]

JONGSUNG = [
    "", "ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ",
    "ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ",
    "ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"
]

# 쌍자음 분해
DOUBLE_CONSONANT = {
    "ㄲ": ["ㄱ","ㄱ"],
    "ㄸ": ["ㄷ","ㄷ"],
    "ㅃ": ["ㅂ","ㅂ"],
    "ㅆ": ["ㅅ","ㅅ"],
    "ㅉ": ["ㅈ","ㅈ"]
}

# 겹받침 분해
DOUBLE_JONG = {
    "ㄳ": ["ㄱ","ㅅ"],
    "ㄵ": ["ㄴ","ㅈ"],
    "ㄶ": ["ㄴ","ㅎ"],
    "ㄺ": ["ㄹ","ㄱ"],
    "ㄻ": ["ㄹ","ㅁ"],
    "ㄼ": ["ㄹ","ㅂ"],
    "ㄽ": ["ㄹ","ㅅ"],
    "ㄾ": ["ㄹ","ㅌ"],
    "ㄿ": ["ㄹ","ㅍ"],
    "ㅀ": ["ㄹ","ㅎ"],
    "ㅄ": ["ㅂ","ㅅ"]
}

# 모음 분해 규칙
VOWEL_RULE = {
    "ㅏ": ["ㅏ"],
    "ㅑ": ["ㅑ"],
    "ㅐ": ["ㅐ"],
    "ㅔ": ["ㅔ"],
    "ㅖ": ["ㅖ"],
    "ㅓ": ["ㅏ"],
    "ㅕ": ["ㅑ"],
    "ㅗ": ["ㅏ"],
    "ㅛ": ["ㅑ"],
    "ㅜ": ["ㅏ"],
    "ㅠ": ["ㅑ"],
    "ㅡ": ["ㅣ"],
    "ㅚ": ["ㅏ","ㅣ"],
    "ㅟ": ["ㅏ","ㅣ"],
    "ㅢ": ["ㅣ","ㅣ"],
    "ㅣ": ["ㅣ"]
}

# ===============================
# 한글 분해 함수
# ===============================

def decompose_hangul(char):
    result = []

    # 이미 자모로 입력된 경우
    if char in DOUBLE_CONSONANT:
        return DOUBLE_CONSONANT[char]

    if char in DOUBLE_JONG:
        return DOUBLE_JONG[char]

    if char in VOWEL_RULE:
        return VOWEL_RULE[char]

    code = ord(char) - 0xAC00
    if code < 0 or code > 11171:
        return [char]

    cho = code // 588
    jung = (code % 588) // 28
    jong = code % 28

    # 초성
    c = CHOSUNG[cho]
    if c in DOUBLE_CONSONANT:
        result.extend(DOUBLE_CONSONANT[c])
    else:
        result.append(c)

    # 중성
    result.extend(VOWEL_RULE.get(JUNGSUNG[jung], []))

    # 종성
    if jong != 0:
        j = JONGSUNG[jong]
        if j in DOUBLE_JONG:
            result.extend(DOUBLE_JONG[j])
        elif j in DOUBLE_CONSONANT:
            result.extend(DOUBLE_CONSONANT[j])
        else:
            result.append(j)

    return result

# ===============================
# 메인 로직
# ===============================

def count_characters(text):
    counter = Counter()

    for char in text.replace(" ", ""):
        # 영어
        if char.isalpha() and char.encode().isalpha():
            counter[char.upper()] += 1

        # 한글
        elif "가" <= char <= "힣" or char in CHOSUNG or char in JUNGSUNG or char in JONGSUNG:
            parts = decompose_hangul(char)
            for p in parts:
                counter[p] += 1

    return counter

# ===============================
# Streamlit UI
# ===============================

st.set_page_config(page_title="와펜 글자 계산기")

st.title("🧵 와펜 글자 개수 계산기 by.와펜마을감씨🍊")
st.write("한글 · 영어 상관없이 입력하면 자동으로 개수를 계산해드립니다.")

text = st.text_input("단어 또는 문장을 입력하시고 엔터를 눌러주세요.")

if text:
    result = count_characters(text)
    st.subheader("📊 계산 결과")

    for k, v in sorted(result.items()):
        st.write(f"{k} : {v}개")
