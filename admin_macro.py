"""python admin_macro.py"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.anyang.go.kr/userJoinStplatAgre.do")
time.sleep(1)

# ✅ 모든 약관 '동의합니다' 클릭 (필수 + 선택)
try:
    for label_for in ['agree', 'agree2', 'agree3', 'agree4']:
        label = driver.find_element(By.CSS_SELECTOR, f"label[for='{label_for}']")
        label.click()
        print(f"✅ 약관 동의 클릭 완료: {label_for}")
except Exception as e:
    print(f"❌ 약관 클릭 실패: {e}")

# ✅ 다음 버튼 클릭
try:
    next_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value*='다음']")
    next_btn.click()
    print("✅ 다음 버튼 클릭 완료")
except Exception as e:
    print(f"❌ 다음 버튼 클릭 실패: {e}")

# ✅ 새 창 전환 (02 회원유형 선택)
try:
    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    print("✅ 회원유형 선택 창으로 전환 완료")
except Exception as e:
    print(f"❌ 창 전환 실패: {e}")

# ✅ 일반회원 가입하기 클릭
try:
    join_btn = driver.find_element(By.XPATH, "//a[@href='/userJoinSelfCrtfc.do?joinTy=native']")
    join_btn.click()
    print("✅ 일반회원 가입하기 클릭 완료")
except Exception as e:
    print(f"❌ 가입하기 클릭 실패: {e}")

# ✅ 본인인증 페이지 새 창 전환
try:
    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    print("✅ 본인인증 창으로 전환 완료")
except Exception as e:
    print(f"❌ 본인인증 창 전환 실패: {e}")

# ✅ 휴대폰 본인인증 버튼 클릭
try:
    time.sleep(3)
    phone_btn = driver.find_element(By.XPATH, "//a[contains(@onclick,'openKMCISWindow')]")
    phone_btn.click()
    print("✅ 휴대폰 본인인증 버튼 클릭 완료")
except Exception as e:
    print(f"❌ 휴대폰 본인인증 클릭 실패: {e}")

# ✅ 팝업창에서 SMS 인증 버튼 클릭
try:
    time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    print("✅ 인증 팝업창 전환 완료")

    sms_btn = driver.find_element(By.CSS_SELECTOR, "li.sms button.certAuthCheck")
    driver.execute_script("arguments[0].click();", sms_btn)
    print("✅ SMS 인증 버튼 클릭 완료")
except Exception as e:
    print(f"❌ SMS 인증 클릭 실패: {e}")

# ✅ 마지막 확인용 대기
input("✅ 수동 확인을 위해 브라우저를 유지합니다. 엔터 누르면 닫힙니다.")
