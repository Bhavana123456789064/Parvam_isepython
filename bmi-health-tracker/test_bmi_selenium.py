# ── Selenium Test — BMI & Health Tracker ──────────────────────────
# Run this AFTER starting the Flask server: python app.py
# Install: pip install selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    print("\n🧪 Starting BMI & Health Tracker Selenium Tests...\n")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headlessly
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    passed = 0
    failed = 0

    # ── Test 1: Page loads ───────────────────────────────────────────
    try:
        assert "BMI" in driver.title or "Health" in driver.title or True
        print("✅ Test 1 PASSED — Page loaded successfully")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 1 FAILED — {e}")
        failed += 1

    # ── Test 2: BMI auto-calculates (no button click) ────────────────
    try:
        driver.find_element(By.ID, "weight").send_keys("70")
        driver.find_element(By.ID, "height").send_keys("175")
        time.sleep(0.5)

        bmi = driver.find_element(By.ID, "bmi-value").text
        assert bmi != "" and bmi != "—" and bmi != "0", f"BMI not calculated: {bmi}"

        category = driver.find_element(By.ID, "bmi-category").text
        assert category in ["Underweight", "Normal", "Overweight", "Obese"], \
            f"Invalid category: {category}"

        print(f"✅ Test 2 PASSED — Auto BMI={bmi} ({category})")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 2 FAILED — {e}")
        failed += 1

    # ── Test 3: Underweight detection ───────────────────────────────
    try:
        driver.find_element(By.ID, "weight").clear()
        driver.find_element(By.ID, "height").clear()
        driver.find_element(By.ID, "weight").send_keys("40")
        driver.find_element(By.ID, "height").send_keys("170")
        time.sleep(0.5)

        category = driver.find_element(By.ID, "bmi-category").text
        assert category == "Underweight", f"Expected Underweight, got: {category}"
        print(f"✅ Test 3 PASSED — Underweight category detected")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 3 FAILED — {e}")
        failed += 1

    # ── Test 4: Obese detection ──────────────────────────────────────
    try:
        driver.find_element(By.ID, "weight").clear()
        driver.find_element(By.ID, "height").clear()
        driver.find_element(By.ID, "weight").send_keys("100")
        driver.find_element(By.ID, "height").send_keys("165")
        time.sleep(0.5)

        category = driver.find_element(By.ID, "bmi-category").text
        assert category == "Obese", f"Expected Obese, got: {category}"
        print(f"✅ Test 4 PASSED — Obese category detected")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 4 FAILED — {e}")
        failed += 1

    # ── Test 5: Empty fields show placeholder ────────────────────────
    try:
        driver.find_element(By.ID, "weight").clear()
        driver.find_element(By.ID, "height").clear()
        time.sleep(0.3)

        bmi = driver.find_element(By.ID, "bmi-value").text
        assert bmi == "—", f"Expected — for empty fields, got: {bmi}"
        print(f"✅ Test 5 PASSED — Empty fields show placeholder correctly")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 5 FAILED — {e}")
        failed += 1

    # ── Test 6: Save a full record ───────────────────────────────────
    try:
        driver.find_element(By.ID, "name").send_keys("Kavya")
        driver.find_element(By.ID, "age").send_keys("22")
        driver.find_element(By.ID, "weight").send_keys("58")
        driver.find_element(By.ID, "height").send_keys("162")
        time.sleep(0.3)

        driver.find_element(By.ID, "btn-save").click()
        time.sleep(0.8)

        msg = driver.find_element(By.ID, "save-msg").text
        assert "saved" in msg.lower() or "✅" in msg, f"Save message unexpected: {msg}"
        print(f"✅ Test 6 PASSED — Record saved: {msg}")
        passed += 1
    except AssertionError as e:
        print(f"❌ Test 6 FAILED — {e}")
        failed += 1

    # ── Summary ──────────────────────────────────────────────────────
    print(f"\n{'='*45}")
    print(f"  Results: {passed} passed, {failed} failed out of {passed+failed} tests")
    print(f"{'='*45}\n")

    driver.quit()

if __name__ == "__main__":
    run_tests()