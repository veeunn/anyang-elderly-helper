import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.set_page_config(page_title="행정인턴 어르신 도우미", layout="centered")
st.title("📋 행정인턴 업무 자동화 어르신 도우미")

uploaded_file = st.file_uploader("📷 신분증 이미지를 업로드하세요 (주민등록증, 운전면허증)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 신분증", use_container_width=True)

    with st.spinner("🔍 OCR 인식 중..."):
        reader = easyocr.Reader(['ko', 'en'])
        results = reader.readtext(np.array(image), detail=1)  # (box, text, confidence)

    # 신분증 종류 판별
    is_license = any("운전면허" in text or "Driver" in text for (_, text, _) in results)

    name, birth, gender_code, address = "", "", "", ""

    # 정제된 텍스트 리스트 (y축 좌표 기준으로 정렬)
    results_sorted = sorted(results, key=lambda x: x[0][0][1])  # 좌상단 y좌표 기준

    # 이름 추출 (운전면허증일 경우, 주민번호 위에 있는 한글 이름)
    for i, (box, text, conf) in enumerate(results_sorted):
        if re.match(r"\d{6}[-\s]?\d{7}", text):  # 주민번호
            birth_match = re.match(r"(\d{6})[-\s]?(\d{7})", text)
            birth = birth_match.group(1)
            gender_code = birth_match.group(2)[0]

            # 그 위 텍스트는 이름일 가능성 높음
            if i >= 1:
                name_candidate = results_sorted[i-1][1]
                if re.match(r"[가-힣]{2,4}", name_candidate):
                    name = name_candidate
            break

    # 주소 추출: 주민번호보다 아래에 있고 "구"나 "로", "길", "동" 포함하는 한글 텍스트
    for (box, text, conf) in results_sorted:
        y = box[0][1]
        if y > 250 and any(kw in text for kw in ["구", "로", "동", "길", "시", "도", "읍", "면"]):
            if len(text) >= 10 and re.search(r"[가-힣]", text):
                address = text
                break

    if name and birth and gender_code:
        st.success("✅ 인식 완료!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🧑 이름")
            st.code(name)
        with col2:
            st.markdown("### 🎂 생년월일")
            st.code(birth)
        with col3:
            st.markdown("### 🚻 성별코드")
            st.code(gender_code)

        st.markdown("### 🏠 주소")
        st.code(address if address else "주소 인식 실패")

        st.markdown("---")
        st.markdown("### 👉🏻 다음 단계 안내")
        st.markdown("""
        - PASS 본인인증 페이지 열기  
        - 복사한 정보들을 붙여넣기  
        - 휴대폰 번호는 직접 입력
        """)
    else:
        st.error("❌ 인식 실패: 이름 또는 주민번호를 인식하지 못했습니다.")

st.markdown("---")
st.markdown("""
Made by: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))  
""")
