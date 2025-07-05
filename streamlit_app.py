import streamlit as st
from PIL import Image
import easyocr
import re
import numpy as np

st.set_page_config(page_title="행정인턴 어르신 도우미", layout="centered")
st.title("📋 행정인턴 업무 자동화 어르신 도우미")

st.markdown("""
이 도구는 어르신의 신분증 사진에서 **이름, 생년월일, 성별코드(1 또는 2)** 를 자동으로 추출하여,
**안양시청 PASS 본인인증 페이지**에 빠르게 붙여넣을 수 있도록 도와줍니다.
""")

uploaded_file = st.file_uploader("📷 신분증 사진을 업로드하세요 (주민등록증, 운전면허증 등)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 신분증", use_container_width=True)

    with st.spinner("🔍 텍스트 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'], gpu=False)
        image_np = np.array(image)  # <== 핵심 수정
        result = reader.readtext(image_np)
        text = "\n".join([item[1] for item in result])

    # 이름, 주민번호 추출
    name_match = re.search(r"주민등록증\s*\n*([가-힣]{2,4})", text) or re.search(r"([가-힣]{2,4})", text)
    resno_match = re.search(r"(\d{6})[- ]?(\d{7})", text)

    if name_match and resno_match:
        name = name_match.group(1)
        birth = resno_match.group(1)
        gender_code = resno_match.group(2)[0]

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"이름: {name}")
            st.text_input("이름 복사", value=name, label_visibility="collapsed")

            st.success(f"생년월일: {birth}")
            st.text_input("생년월일 복사", value=birth, label_visibility="collapsed")

            st.success(f"성별 코드: {gender_code}")
            st.text_input("성별 코드 복사", value=gender_code, label_visibility="collapsed")

        with col2:
            st.markdown("""
            ### ✅ 다음 단계 안내:
            - PASS 본인인증 페이지 열기  
            - 복사한 정보들을 해당 칸에 붙여넣기  
            - 휴대폰 번호는 직접 입력  
            """)
    else:
        st.error("❌ 정보를 정확히 인식하지 못했어요. 사진이 선명한지 확인해 주세요.")

st.markdown("---")
st.markdown("💡 만든 사람: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))")
