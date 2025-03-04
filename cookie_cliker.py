from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import os.path
import time
import csv


def cookie_clicker(time_between_buys=15, duration=5):            # Duration in minutes
    """Automates Cookie Clicker and saves the performance in a sorted CSV."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://orteil.dashnet.org/cookieclicker/")
    time.sleep(3)

    # Select Language
    driver.find_element(By.ID, value="langSelect-PT-BR").click()
    time.sleep(3)

    cookie = driver.find_element(By.ID, value="bigCookie")
    start_time = time.time()

    # Time in minutes
    timeout = start_time + 60 * duration

    # Path for the CSV data
    file_path = f"cookie_performance_{duration}.csv"
    file_exists = os.path.exists(file_path)

    # Clicking loop
    while time.time() <= timeout:
        cookie.click()

        if time.time() - start_time > time_between_buys:  # Time between
            buy_upgrades(driver)
            buy_products(driver)
            start_time = time.time()

    cookies_per_second = get_cookies_per_second(driver)
    save_data(file_path, time_between_buys, cookies_per_second, file_exists)
    print(f"cookeis per second: {cookies_per_second}")
    driver.quit()


def buy_products(driver):
    """Buys available upgrades."""
    products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    for product in products[::-1]:
        try:
            product.click()
            time.sleep(0.1)
        except StaleElementReferenceException:
            continue


def buy_upgrades(driver):
    """Buys available products in reverse order (higher priority)."""
    upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
    for upgrade in upgrades:
        try:
            upgrade.click()
            time.sleep(0.1)
        except StaleElementReferenceException:
            continue


def get_cookies_per_second(driver):
    """Returns the current cookies per second"""
    try:
        cookies_per_second = WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="cookiesPerSecond"]'))
        )
        return cookies_per_second.text.split()[2]  # Formats the cookies per second
    except StaleElementReferenceException:
        cookies_per_second = WebDriverWait(driver, 15).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="cookiesPerSecond"]'))
        )
        return cookies_per_second.text.split()[2]  # Formats the cookies per second


def save_data(file_path, time_between_buys, cookies_per_second, file_exists):
    """Saves the data in a sorted CSV file based on time between buys."""
    data = []
    if file_exists:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Save the header
            data = list(reader)

    # Add the new row
    data.append([str(time_between_buys), cookies_per_second])

    # Sort data by "Test Number" (first column) as integer
    data.sort(key=lambda row: int(row[0]) if row and row[0].isdigit() else float('inf'))

    # Write sorted data back to the file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time Between Buys", "Cookies Per Second"])  # Write the header
        writer.writerows(data)

if __name__ == "__main__":
    cookie_clicker(time_between_buys=2, duration=5)
