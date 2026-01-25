from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import os   # ✅ ADDED: needed to safely read files from folder

driver = webdriver.Chrome()
num = 1   # ✅ CHANGED: Amazon pages start from 1, not 0
laptop_quantity = 1

os.makedirs("laptop_data", exist_ok=True)   # ✅ ADDED: create folder safely (no apostrophe)

while num < 4:
    web = f"https://www.amazon.in/s?k=laptop&page={num}"
    driver.get(web)
    time.sleep(5)   # ✅ CHANGED: slightly more wait for dynamic load

    # here we are getting every single laptop html code together 
    laptops_raw = driver.find_elements(By.CSS_SELECTOR, "div.puis-card-container")  
    # ✅ CHANGED: CLASS_NAME → CSS_SELECTOR (supports multi-class safely)

    print(len(laptops_raw))

    for laptop_raw in laptops_raw:
        laptop = laptop_raw.get_attribute("outerHTML")

        file = f"laptop_data/laptop_{laptop_quantity}_page_{num}.html"  
        # ✅ CHANGED: removed apostrophe + fixed filename format

        with open(file, "w", encoding="utf-8") as w:
            w.write(laptop)

        laptop_quantity += 1

    num += 1

driver.quit()   # ✅ ADDED: close browser properly

# now we will get the data from the saved files
folder = "laptop_data"   # ✅ ADDED: folder variable instead of hardcoding
csv_file = f"laptop_data/laptop_data.csv"

for filename in os.listdir(folder):   # ✅ CHANGED: loop through real existing files
    file_path = os.path.join(folder, filename)   # ✅ ADDED: safe path join

    with open(file_path, "r", encoding="utf-8") as f:   # ✅ ADDED: read HTML file properly
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")   # ✅ CHANGED: parse actual HTML, not filename

    name_tag = soup.find("h2")   # ✅ ADDED: avoid crash if tag missing
    price_tag = soup.find("span", class_="a-price-whole")   # ✅ ADDED
    mrp_tag = soup.find("span", class_="a-offscreen")   # ✅ ADDED

    if not name_tag or not price_tag or not mrp_tag:   # ✅ ADDED: safety check
        print("Skipping broken file:", filename)
        continue

    name_of_laptop = name_tag.text.strip()   # ✅ CHANGED: cleaned text
    with_discount_price_of_laptop = price_tag.text.strip()   # ✅ CHANGED
    with_no_discount_price_of_laptop = mrp_tag.text.strip()   # ✅ CHANGED

    with open(csv_file,"a",newline="",encoding="utf-8")as a:
        writer = csv.writer(a)
        writer.writerow([name_of_laptop,with_discount_price_of_laptop,with_no_discount_price_of_laptop])
    print(f"name of the laptop is: {name_of_laptop}")
    print(f"price of the laptop is with discount: {with_discount_price_of_laptop}")
    print(f"price of the laptop is not with discount: {with_no_discount_price_of_laptop}")
    print("-" * 50)   # ✅ ADDED: readability




