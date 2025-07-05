import streamlit as st
from PIL import Image
import easyocr
import re
from streamlit.components.v1 import html
import numpy as np

# ✅ 클립보드 복사 버튼 함수 (JS 기반)
def copy_to_clipboard_js(text, key):
    escaped_text = text.replace("'", "\\'")
    html(f"""
    <div style="margin-top: 4px;">
        <button onclick="navigator.clipboard.writeText('{escaped_text}'); alert('{escaped_text} 복사 완료!');">
            📋 복사
        </button>
    </div>
    """, height=40, key=key)

# ✅ OCR Reader 초기화
reader = easyocr.Reader(['ko', 'en'])

# ✅ 페이지 설정
st.set_page_config(page_title="행정인턴 어르신 도우미", layout="centered")
st.title("📋 행정인턴 업무 자동화 어르신 도우미")

st.markdown("""
이 도구는 어르신의 신분증 사진에서 **이름, 생년월일, 성별코드(1 또는 2)** 를 자동으로 추출하여  
**안양시청 PASS 본인인증 페이지**에 빠르게 붙여넣을 수 있도록 도와줍니다.
""")

# ✅ 파일 업로더
uploaded_file = st.file_uploader("📷 신분증 사진을 업로드하세요 (주민등록증, 운전면허증 등)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 신분증", use_column_width=True)

    with st.spinner("🔍 텍스트 인식 중..."):
        image_array = np.array(image)
        result = reader.readtext(image_array)

    text = "\n".join([item[1] for item in result])

    name_match = re.search(r"([가-힣]{2,4})", text)
    resno_match = re.search(r"(\d{6})[- ]?(\d{7})", text)

    if name_match and resno_match:
        name = name_match.group(1)
        birth = resno_match.group(1)
        gender_code = resno_match.group(2)[0]

        st.success("✅ 인식 완료!")

        # 🔹 이름
        st.markdown("### 🧑 이름")
        st.code(name, language="text")
        copy_to_clipboard_js(name, key="copy_name")

        # 🔹 생년월일
        st.markdown("### 🎂 생년월일")
        st.code(birth, language="text")
        copy_to_clipboard_js(birth, key="copy_birth")

        # 🔹 성별코드
        st.markdown("### 🚻 성별 코드")
        st.code(gender_code, language="text")
        copy_to_clipboard_js(gender_code, key="copy_gender")

        st.markdown("---")
        st.markdown("""
        ### ✅ 다음 단계 안내:
        - PASS 본인인증 페이지 열기  
        - 복사한 정보들을 해당 칸에 붙여넣기  
        - 휴대폰 번호는 직접 입력
        """)

    else:
        st.error("❌ 이름이나 주민등록번호 인식 실패! 사진을 다시 찍거나 선명도를 확인해주세요.")

# 👤 제작자 정보
st.markdown("---")
st.markdown("""
Made by: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))  
""")
