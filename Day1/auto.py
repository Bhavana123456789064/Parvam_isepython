from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Credentials
EMAIL = "your_email_here"
PASSWORD = "your_password_here"

# ✅ START POINT (Login Page)
START_URL = "https://scholar.parvam.in/student/login"

# ✅ END POINT (Expected after login - dashboard)
END_URL_PART = "https://scholar.parvam.in/student/dashboard"   # adjust if needed

# Open browser
driver = webdriver.Chrome()
driver.get(START_URL)

wait = WebDriverWait(driver, 15)

# Enter login details
email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))

email_field.send_keys(EMAIL)
password_field.send_keys(PASSWORD)

# Click Sign In
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Sign')]")))
login_button.click()

# ✅ END POINT CHECK (2 methods)

# Method 1: URL contains "dashboard"
wait.until(EC.url_contains(END_URL_PART))

# Method 2 (optional, stronger): wait for dashboard element
# wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Dashboard')]")))

print("✅ Login successful and reached end point")

# Close browser
driver.quit()