import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = 'chromedriver.exe'  # Путь к ChromeDriver

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('window-size=1200x600') 

# Логин и пароль
avito_login = "LOGIN"

# Сервис ChromeDriver
service = Service(chrome_driver_path)

# веб-драйвера
driver = webdriver.Chrome(service=service, options=options)

try:
    # В ходе выполнения алгоритма было выявлено, что при переходе на карточку товара открывается новая вкладка без токена авторизации
    # Предлагаю изменить алгоритм действий и провести авторизацию после нажатия кнопки заказа товара
    # Если необходимо произвести все действия по ТЗ, то необходимо раскомментировать код ниже.
    """
    # Авторизация на сайте Avito
    driver.get('https://www.avito.ru/profile/login')
    time.sleep(2)  # Задержка для визуализации
    driver.find_element(By.NAME, 'login').send_keys(avito_login)
    driver.find_element(By.NAME, 'password').send_keys(avito_password)
    time.sleep(2)  # Задержка для визуализации
    driver.find_element(By.CSS_SELECTOR, 'button[data-marker="login-form/submit"]').click()
    time.sleep(30)  # Задержка для ввода капчи и СМС
    
    # Ожидание перехода на главную страницу после авторизации
    WebDriverWait(driver, 10).until(EC.url_contains('https://www.avito.ru/'))
    time.sleep(2)  # Задержка для визуализации
    """
    # Переход на страницу "Личные вещи" с доставкой
    driver.get('https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1')
    time.sleep(2)  # Задержка для визуализации

    # Выбор первого объявления из списка
    first_ad = driver.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]')
    first_ad.click()
    time.sleep(2)  # Задержка для визуализации

    # Переключение на новую вкладку
    driver.switch_to.window(driver.window_handles[-1])

    # Переход к оформлению заказа с доставкой
    buy_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-marker="delivery-item-button-main"]'))
    )
    buy_button.click()
    time.sleep(2)  # Задержка для визуализации
    # Авторизация на сайте Avito
    driver.find_element(By.NAME, 'login').send_keys(avito_login)
    driver.find_element(By.NAME, 'password').send_keys(avito_password)
    time.sleep(2)  # Задержка для визуализации
    driver.find_element(By.CSS_SELECTOR, 'button[data-marker="login-form/submit"]').click()
    time.sleep(30)  # Задержка для ввода капчи и СМС
    # Проверка, что поле телефона пустое
    phone_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="phone"]'))
    )
    phone_value = phone_field.get_attribute('value')
    assert phone_value == '', 'Поле телефона не пустое'
    if phone_value == 0 or phone_value == '':
        print('Телефон пустой')
   
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()