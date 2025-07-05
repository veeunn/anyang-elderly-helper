import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from streamlit.components.v1 import html

# EasyOCR Reader 초기화
reader = easyocr.Reader(['ko'], gpu=False)

st.title("📋 행정인턴 업무 자동화 어르신 도우미")
st.write("이 도구는 어르신의 신분증 사진에서 이름, 생년월일, 성별코드(1 또는 2)를 자동으로 추출하여, 안양시청 PASS 본인인증 페이지에 빠르게 붙여넣을 수 있도록 도와줍니다.")

uploaded_file = st.file_uploader("📷 신분증 사진을 업로드하세요 (주민등록증, 운전면허증 등)", type=["png", "jpg", "jpeg"])

# 복사 버튼 함수 (JS 기반)
def copy_to_clipboard_js(text, key):
    html(f"""
        <div style="margin-top: 4px;">
            <button onclick="navigator.clipboard.writeText('{text}')"
                    style="padding:4px 10px;border-radius:6px;background:#f0f2f6;border:none;cursor:pointer;">
                📋 복사
            </button>
        </div>
    """, key=key)

# 신분증 종류 탐지 함수
def detect_card_type(texts):
    full_text = " ".join([t[1] for t in texts])
    if '주민등록증' in full_text:
        return '주민등록증'
    elif '운전면허' in full_text or 'Driver' in full_text:
        return '운전면허증'
    else:
        return '알 수 없음'

# 이름, 생년월일, 성별코드 추출 함수
def extract_info(texts):
    lines = [t[1] for t in texts]
    name = ""
    id_number = ""

    for i, line in enumerate(lines):
        # 주민번호 탐색
        if '-' in line:
            parts = line.split('-')
            if len(parts) == 2 and len(parts[0]) == 6 and parts[0].isdigit():
                id_number = line.strip()
                if i > 0:
                    name = lines[i - 1].strip()
                break

    birth = id_number.split('-')[0] if id_number else ""
    gender = id_number.split('-')[1][0] if id_number else ""

    return name, birth, gender

# 메인 실행
if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        st.image(image, caption="업로드한 신분증", use_container_width=True)
        with st.spinner("🔍 텍스트 인식 중..."):
            result = reader.readtext(image_np)

        st.success("✅ 인식 완료!")

        card_type = detect_card_type(result)
        st.markdown(f"📄 **신분증 종류:** {card_type}")

        name, birth, gender = extract_info(result)

        st.markdown("### 🧑 이름")
        st.write(name)
        copy_to_clipboard_js(name, key="copy_name")

        st.markdown("### 🎂 생년월일")
        st.write(birth)
        copy_to_clipboard_js(birth, key="copy_birth")

        st.markdown("### 🚻 성별코드")
        st.write(gender)
        copy_to_clipboard_js(gender, key="copy_gender")

    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")

# 👤 제작자 정보
st.markdown("---")
st.markdown("""
Made by: 황예은 (GitHub: [@veeunn](https://github.com/veeunn))  
""")
