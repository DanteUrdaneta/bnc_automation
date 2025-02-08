from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas
import time


coordenada_ruta = 'cordenadas.csv'
credenciales_ruta = 'credenciales.csv'


df = pandas.read_csv(coordenada_ruta, dtype=str)
credenciales = pandas.read_csv(credenciales_ruta, dtype=str)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://personas.bncenlinea.com/Auth/Login")

time.sleep(5)


def  login(credenciales):
  login_buttons = ['CardNumber', 'UserID', 'BtnSend', 'UserPassword']
  login_credentials = ['5410360004255395','28391082','10102020Dl.']

  cardnumber = driver.find_element(By.NAME, login_buttons[0])
  cardnumber.send_keys(credenciales['cuenta'])

  userid = driver.find_element(By.ID, login_buttons[1])
  userid.send_keys(credenciales['cedula'])

  button = driver.find_element(By.ID, login_buttons[2])
  button.click()

  time.sleep(1)

  password = driver.find_element(By.NAME, login_buttons[3])
  password.send_keys(credenciales['password'])

  button = driver.find_element(By.ID, login_buttons[2])
  button.click()
  
def debitar_bs_cuenta():
  cuenta = driver.find_element(By.XPATH, "//button[@data-id='idAccount_VES']")
  cuenta.click()
  time.sleep(1)
  option = driver.find_element(By.ID, 'bs-select-1-1')
  option.click()

  
def us_cuenta():
  cuenta = driver.find_element(By.XPATH, "//button[@data-id='idAccount_Currency']")
  cuenta.click()
  time.sleep(1)
  option = driver.find_element(By.ID, 'bs-select-2-1')
  option.click()
  
  
def monto(usd):
  input = driver.find_element(By.ID, 'Amount_Currency')
  input.send_keys(usd)
  element = driver.find_element(By.XPATH, """//*[@id="Frm_Purchase_DoOperation"]/div/div[9]/div/div[1]/button""")
  element.click()

def confirmar():
    element = driver.find_element(By.XPATH, """//*[@id="Frm_Purchase_Verify"]/div/div[9]/div/div[1]/button""")
    element.click()
    control = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ControlNumber"))
)
    control.send_keys('54713322') # PONER NUMERO DE CONTROL DE LAS CORDENADAS
    cordenada = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, """//*[@id="Frm_AuthFactor_Set"]/div/div/div[2]/div/div/div/div/div/span""")))    
    cor = cordenada.text #example D-9
    # separar la cordenada
    cordenadas = cor.split('-')
    cor = df.loc[int(cordenadas[1])-1, cordenadas[0]]
    print(cor)
    input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "Value"))
    )
    input.send_keys(cor)
    
    submit = driver.find_element(By.XPATH, """//*[@id="Mdl-Content2"]/div/div/div[2]/div[2]/button[1]""")
    submit.click()
    
  
login(credenciales)

time.sleep(1)




while True:
  
  driver.get('https://personas.bncenlinea.com/ForeignExchange/ForeignExchange/Purchase')

  try:
    time.sleep(1)
    debitar_bs_cuenta()
    us_cuenta()

    monto(20)
    time.sleep(1)
    confirmar()
    time.sleep(1)

  except:
    print('error')
    driver.get('https://personas.bncenlinea.com/ForeignExchange/ForeignExchange/Purchase')