from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas
import time


coordenada_ruta = 'cordenadas.csv'
credenciales_ruta = 'credenciales.csv'

df = pandas.read_csv(coordenada_ruta, dtype=str)
credenciales = pandas.read_csv(credenciales_ruta, dtype=str).iloc[0]  # Tomamos solo una fila

def crear_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", False)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login(driver, credenciales):
    driver.get("https://personas.bncenlinea.com/Auth/Login")
    time.sleep(5)
    login_buttons = ['CardNumber', 'UserID', 'BtnSend', 'UserPassword']

    driver.find_element(By.NAME, login_buttons[0]).send_keys(credenciales['cuenta'])
    driver.find_element(By.ID, login_buttons[1]).send_keys(credenciales['cedula'])
    driver.find_element(By.ID, login_buttons[2]).click()

    time.sleep(1)
    driver.find_element(By.NAME, login_buttons[3]).send_keys(credenciales['password'])
    driver.find_element(By.ID, login_buttons[2]).click()

def debitar_bs_cuenta(driver):
    driver.find_element(By.XPATH, "//button[@data-id='idAccount_VES']").click()
    time.sleep(1)
    driver.find_element(By.ID, 'bs-select-1-1').click()

def us_cuenta(driver):
    driver.find_element(By.XPATH, "//button[@data-id='idAccount_Currency']").click()
    time.sleep(1)
    driver.find_element(By.ID, 'bs-select-2-1').click()

def monto(driver, usd):
    driver.find_element(By.ID, 'Amount_Currency').send_keys(usd)
    driver.find_element(By.XPATH, """//*[@id="Frm_Purchase_DoOperation"]/div/div[9]/div/div[1]/button""").click()

def confirmar(driver):
    driver.find_element(By.XPATH, """//*[@id="Frm_Purchase_Verify"]/div/div[9]/div/div[1]/button""").click()
    time.sleep(3)
    try:
        control = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ControlNumber")))
        control.send_keys('29305558')  # PONER NUMERO DE CONTROL

        cordenada = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, """//*[@id="Frm_AuthFactor_Set"]/div/div/div[2]/div/div/div/div/div/span""")))
        cor = cordenada.text.split('-')
        valor = df.loc[int(cor[1]) - 1, cor[0]]
        print(f"Poniendo coordenadas {valor}")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Value"))).send_keys(valor)
        driver.find_element(By.XPATH, """//*[@id="Mdl-Content2"]/div/div/div[2]/div[2]/button[1]""").click()
        print('Compra exitosa')
        time.sleep(1)
    except:
        driver.find_element(By.XPATH, """//*[@id="Mdl-Content2"]/div/div/div[2]/div[2]/button[1]""").click()
        print('Compra exitosa (sin coordenada)')
        time.sleep(1)

# Bucle principal
while True:
    try:
        driver = crear_driver()
        login(driver, credenciales)
        time.sleep(2)
        driver.get('https://personas.bncenlinea.com/ForeignExchange/ForeignExchange/Purchase')
        time.sleep(2)

        debitar_bs_cuenta(driver)
        us_cuenta(driver)
        monto(driver, "20")  # Puedes cambiar el monto aquí
        confirmar(driver)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        print("Cerrando navegador y esperando 5 minutos...")
        driver.quit()
        time.sleep(300)
