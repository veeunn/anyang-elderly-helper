import streamlit as st
from PIL import Image
import easyocr
import re
import numpy as np

st.set_page_config(page_title="행정인턴 어르신 도우미", layout="centered")
st.title("📋 행정인턴 업무 자동화 어르신 도우미")

st.markdown("""
이 도구는 어르신의 신분증 사진에서 **이름, 생년월일, 성별코드(1 또는 2), 주소** 를 자동으로 추출하여,  
**안양시청 PASS 본인인증 페이지**에 빠르게 붙여넣을 수 있도록 도와줍니다.
""")

uploaded_file = st.file_uploader("📷 신분증 사진을 업로드하세요 (주민등록증, 운전면허증)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 신분증", use_container_width=True)

    with st.spinner("🔍 텍스트 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'])
        result = reader.readtext(np.array(image))
        texts = [item[1] for item in result]
        text_joined = "\n".join(texts)

    # 신분증 종류 판별
    is_license = any("운전면허" in t or "Driver" in t for t in texts)
    is_idcard = any("주민등록" in t for t in texts)

    # 공통 정보
    name = ""
    birth = ""
    gender_code = ""
    address = ""

    # 이름 추출
    name_candidates = re.findall(r"[가-힣]{2,4}", text_joined)
    for cand in name_candidates:
        if not any(x in cand for x in ["주민", "등록", "증", "자동", "운전", "면허", "장기", "초점", "기증"]):
            name = cand
            break

    # 주민번호 추출
    resno_match = re.search(r"(\d{6})[- ]?(\d{7})", text_joined)
    if resno_match:
        birth = resno_match.group(1)
        gender_code = resno_match.group(2)[0]

    # 주소 추출
    if is_license:
        # 운전면허증 주소: "시" 또는 "구"로 끝나는 라인 중 가장 긴 것
        for line in texts:
            if any(kw in line for kw in ["시", "도", "구", "로", "길", "동", "읍", "면"]):
                if len(line) > 10:
                    address = line.strip()
                    break
    else:
        # 주민등록증 주소
        for line in texts:
            if any(kw in line for kw in ["시", "도", "구", "로", "길", "동", "읍", "면"]) and len(line) > 10:
                address = line.strip()
                break

    if name and birth and gender_code:
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
            st.code(gender_code, language="text")

        st.markdown("### 🏠 주소")
        if address:
            st.code(address, language="text")
        else:
            st.warning("⚠️ 주소를 인식하지 못했습니다.")

        st.markdown("---")
        st.markdown("""
        ### ✅ 다음 단계 안내:
        - PASS 본인인증 페이지 열기  
        - 복사한 정보들을 해당 칸에 붙여넣기  
        - 휴대폰 번호는 직접 입력
        """)
    else:
        st.error("❌ 이름 또는 주민번호 인식 실패! 사진 선명도를 확인해주세요.")

st.markdown("---")
st.markdown("Made by: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))")
