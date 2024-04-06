import random
from selenium import webdriver # Импорт основного драйвера
from selenium.webdriver.common.keys import Keys # Класс клавиш клавиатуры
from selenium.webdriver.common.by import By # Класс поиска с помощью чего..
from selenium.webdriver.firefox.options import Options # Класс опций передаваемых драйверу
from selenium.webdriver.support.ui import WebDriverWait # Класс ожидания
from selenium.webdriver.support import expected_conditions as EC # Класс ожидаемых события
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]
user_agent = random.choice(user_agents)

options = uc.ChromeOptions()
#options.add_argument("headless")
options.add_argument("start-maximized")
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 2})
options.binary_location = ("/opt/chrome-linux64/chrome") 
driver = uc.Chrome(options=options)
