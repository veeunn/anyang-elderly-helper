import streamlit as st
from PIL import Image
import numpy as np
import easyocr
import re

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
    image_np = np.array(image)

    with st.spinner("🔍 텍스트 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'], gpu=False)
        result = reader.readtext(image_np)
        text = "\n".join([item[1] for item in result])

    # ✅ 이름 추출
    lines = text.split("\n")
    name = None
    for i, line in enumerate(lines):
        if "주민등록증" in line or "운전면허증" in line:
            for j in range(i + 1, min(i + 4, len(lines))):
                candidate = lines[j].strip()
                if re.fullmatch(r"[가-힣]{2,4}", candidate):
                    name = candidate
                    break
            break

    # ✅ 생년월일 및 성별 코드 추출
    resno_match = re.search(r"(\d{6})[- ]?(\d{7})", text)

    if name and resno_match:
        birth = resno_match.group(1)
        gender_code = resno_match.group(2)[0]

        st.success("✅ 정보 추출 성공!")

        # 복사 UI
        def copy_value(label, value, key):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text_input(label, value=value, key=key)
            with col2:
                if st.button(f"📋 복사", key=f"copy_{key}"):
                    st.toast(f"{label} 복사됨: {value}", icon="✅")

        copy_value("🧾 이름", name, "name")
        copy_value("📅 생년월일", birth, "birth")
        copy_value("⚧ 성별코드", gender_code, "gender")

        st.markdown("""
        ### ✅ 다음 단계 안내
        1. [PASS 본인인증 페이지](https://www.kmcert.com/kmcis/web_v5/kmcisHp00.jsp) 열기  
        2. 위의 정보를 복사해서 붙여넣기  
        3. 휴대폰 번호, 인증번호는 직접 입력  
        """)
    else:
        st.error("❌ 이름이나 주민등록번호 인식 실패! 사진을 다시 찍거나 선명도를 확인해주세요.")

st.markdown("---")
st.markdown("""
💡 만든 사람: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))  
""")

