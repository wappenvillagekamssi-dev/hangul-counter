import streamlit as st
from collections import defaultdict

CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
JUNG = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
JONG = ["", "ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

vowel_map = {
    "ㅏ": ["ㅏ"], "ㅑ": ["ㅑ"], "ㅐ": ["ㅐ"], "ㅔ": ["ㅔ"], "ㅖ": ["ㅖ"], "ㅣ": ["ㅣ"],
    "ㅓ": ["ㅏ"], "ㅕ": ["ㅑ"], "ㅗ": ["ㅏ"], "ㅛ": ["ㅑ"], "ㅜ": ["ㅏ"], "ㅠ": ["ㅑ"],
    "ㅡ": ["ㅣ"], "ㅚ": ["ㅏ","ㅣ"], "ㅟ": ["ㅏ","ㅣ"], "ㅘ": ["ㅏ","ㅏ"],
    "ㅙ": ["ㅏ","ㅐ"], "ㅝ": ["ㅏ","ㅏ"], "ㅞ": ["ㅏ","ㅔ"], "ㅢ": ["ㅣ","ㅣ"]
}

def count_jamo(text):
    count = defaultdict(int)
    for ch in text:
        if not ("가" <= ch <= "힣"):
            continue
        idx = ord(ch) - 0xAC00
        count[CHO[idx // 588]] += 1
        for v in vowel_map[JUNG[(idx % 588) // 28]]:
            count[v] += 1
        jong = JONG[idx % 28]
        if jong:
            count[jong] += 1
    return dict(count)

st.title("한글 자음·모음 개수 계산기")
text = st.text_input("문구를 입력하세요")

if text:
    result = count_jamo(text)
    st.subheader("결과")
    for k, v in sorted(result.items()):
        st.write(f"{k} : {v}")
