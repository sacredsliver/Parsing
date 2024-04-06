import os
import requests
import time
from auchan.selen import *
from bs4 import BeautifulSoup

def save_image(image_url: str, image_folder: str) -> str:
    folder = image_folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(image_url, stream=True)
    image_path = os.path.join(folder, image_url.split("/")[-1])
    with open(image_path, 'wb') as out_file:
        for chunk in response.iter_content(1024):
            out_file.write(chunk)
    return image_path

def goods(keyword: str) -> list:
    url = "https://www.auchan.ru"
    driver.get(url)
    time.sleep(4)
    #wait = WebDriverWait(driver, 5)
    # wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
    input = driver.find_element(By.ID, "search")
    input.send_keys(keyword)
    input.send_keys(Keys.ENTER)
    time.sleep(3)
    quantity = int(driver.find_element(By.CLASS_NAME, "digi-products__quantity").text)
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//div[@class="digi-tips-title"]')).double_click().perform()
    time.sleep(2)
    counter = 0
    while True:
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        goods_counter = len(driver.find_elements(By.XPATH, '//div[@class="digi-product"]'))
        print("\033c")
        print(f"СКРЕЙПИНГ: {goods_counter} из {quantity} товаров {keyword}")
        if goods_counter >= quantity:
            break
        elif counter > quantity/10:
            break
        else: counter += 1

    driver.execute_script("window.scrollBy(0, 2000)")
    cards = BeautifulSoup(driver.page_source, 'html.parser').find_all("div", class_="digi-product")
    cards_list = []
    for i, card in enumerate(cards):
        card_dict = {}
        card_dict["_id"] = int(card.find("div", class_="digi-product__button").get("productid"))
        card_dict["name"] = card.find("a", class_ ="digi-product__label").getText().strip()
        card_dict["price"] = float(card.find("span", class_="digi-product-price-variant").getText().replace("₽", "").replace("\xa0", "").strip().replace(",", "."))
        image_path = save_image(card.find("img").get("src"), keyword)
        card_dict["image"] = "[Photo](" + image_path + ")"
        card_dict["link"] = "[Link](" + url + card.find("a").get("href") + ")<br>"
        cards_list.append(card_dict)
        print("\033c")
        print(f"ПАРСИНГ: {i} из {len(cards)} товаров {keyword}")
    
    return cards_list


if __name__ == "__main__":

    print(goods("смартфон"))
