import streamlit as st
from PIL import Image
import easyocr
import re
import numpy as np

# 페이지 설정
st.set_page_config(page_title="행정인턴 어르신 도우미", layout="centered")
st.title("📋 행정인턴 업무 자동화 어르신 도우미")

st.markdown("""
이 도구는 어르신의 신분증 사진에서 **이름, 생년월일, 성별코드(1 또는 2), 주소**를 자동으로 추출하여,  
**안양시청 PASS 본인인증 페이지**에 빠르게 붙여넣을 수 있도록 도와줍니다.
""")

uploaded_file = st.file_uploader("📷 신분증 사진을 업로드하세요 (주민등록증, 운전면허증 등)", type=["png", "jpg", "jpeg"])

# 주요 정보 추출 함수
def extract_info_robust(text):
    name = ""
    birth = ""
    gender = ""
    address = ""

    lines = text.split('\n')

    # 주민번호 찾기 → 이름은 그 위줄
    for i, line in enumerate(lines):
        match = re.search(r"(\d{6})[- ]?(\d{7})", line)
        if match:
            birth = match.group(1)
            gender = match.group(2)[0]

            # 위에 줄이 한글 2~4글자면 이름 후보
            if i > 0:
                cand = lines[i - 1].strip()
                if 2 <= len(cand) <= 4 and all('\uac00' <= c <= '\ud7a3' for c in cand):
                    name = cand
            break

    # 주소 추출 (도로명 주소 or 지번 형태)
    for line in lines:
        if any(x in line for x in ["시", "도", "구", "동", "로", "길"]):
            if len(line.strip()) > 8:
                address = line.strip()
                break

    return name, birth, gender, address

# 업로드 시 동작
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 신분증", use_container_width=True)

    with st.spinner("🔍 텍스트 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'])
        result = reader.readtext(np.array(image))
        text = "\n".join([item[1] for item in result])

    # 정보 추출
    name, birth, gender, address = extract_info_robust(text)

    if name and birth and gender:
        st.success("✅ 인식 완료!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🧑 이름")
            st.code(name, language="text")
            
        with col2:
            st.markdown("### 🎂 생년월일")
            st.code(birth, language="text")

        with col3:
            st.markdown("### 🚻 성별코드")
            st.code(gender, language="text")

        # 주소 영역
        st.markdown("### 🏠 주소")
        if address:
            st.code(address, language="text")
        else:
            st.warning("주소를 인식하지 못했습니다. 다시 시도해보세요.")

        st.markdown("---")
        st.markdown("""
        ### ✅ 다음 단계 안내:
        - PASS 본인인증 페이지 열기  
        - 복사한 정보들을 해당 칸에 붙여넣기  
        - 휴대폰 번호는 직접 입력
        """)
    else:
        st.error("❌ 이름이나 주민등록번호 인식 실패! 사진을 다시 찍거나 선명도를 확인해주세요.")

# 하단 제작자 정보
st.markdown("---")
st.markdown("""
💡 만든 사람: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))  
""")
