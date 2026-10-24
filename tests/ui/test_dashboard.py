"""Selenium smoke test; start the app and set AIShIELD_BASE_URL before running."""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("AISHIELD_BASE_URL")
pytestmark = pytest.mark.skipif(not BASE_URL, reason="Set AISHIELD_BASE_URL to a running AIShield instance")


def test_dashboard_runs_security_scan():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(BASE_URL)
        assert "AIShield" in driver.title
        driver.find_element(By.ID, "run-scan").click()
        WebDriverWait(driver, 15).until(
            conditions.text_to_be_present_in_element((By.ID, "scan-status"), "PASS")
        )
        assert driver.find_element(By.ID, "passed-count").text == "5"
        assert len(driver.find_elements(By.CSS_SELECTOR, "#findings-body .status-pass")) == 5
    finally:
        driver.quit()
