import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time
import configparser

config = configparser.ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as configfile:
    config.read_file(configfile)

DISCORD_WEBHOOK_URL = config.get("DEFAULT", "DISCORD_WEBHOOK_URL")
FIREFOX_BINARY_LOCATION = config.get("DEFAULT", "FIREFOX_BINARY_LOCATION")
GECKODRIVER_LOCATION = config.get("DEFAULT", "GECKODRIVER_LOCATION")
USERNAME = config.get("DEFAULT", "USERNAME")
PASSWORD = config.get("DEFAULT", "PASSWORD")
PUBLICO_GERAL = config.get("DEFAULT", "PUBLICO_GERAL", fallback=False)
UNIDADES_SELECIONADAS = config.get("DEFAULT", "UNIDADES_SELECIONADAS").split(",") if config.get("DEFAULT", "UNIDADES_SELECIONADAS") else []

# Configuração do navegador Firefox
options = webdriver.FirefoxOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = FIREFOX_BINARY_LOCATION
options.add_argument("--headless")  # Remova esta linha se quiser visualizar o processo

# Iniciar o WebDriver do Firefox
service = Service(GECKODRIVER_LOCATION)  
driver = webdriver.Firefox(service=service, options=options)


def send_discord_message(content: str):
    payload = {
        "content": content,
        "username": "Notificação Sistema Eletrônico"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Mensagem enviada com sucesso para o Discord")
        else:
            print(f"Erro ao enviar mensagem para o Discord: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Discord: {e}")


# URL da página de login
url_login = "https://centralrelacionamento.sescsp.org.br/?path=login-sesc"
driver.get(url_login)
time.sleep(5)  # Aguarde o carregamento da página

# 🔹 1. Preencher o CPF
cpf_input = driver.find_element(By.NAME, "cpf")
cpf_input.send_keys(USERNAME) 
time.sleep(1)

# 🔹 2. Clicar no botão "CONTINUAR"
btn_continuar = driver.find_element(By.XPATH, "//button[@type='submit']")
btn_continuar.click()
time.sleep(3)  # Aguarde o redirecionamento para a senha

# 🔹 3. Preencher a senha
senha_input = driver.find_element(By.XPATH, "//input[@type='password']")  # Ajuste se necessário
senha_input.send_keys(PASSWORD)
time.sleep(2)

# 🔹 4. Clicar no botão "CONTINUAR" após a senha
btn_continuar_senha = driver.find_element(By.XPATH, "//button[@type='submit']")
btn_continuar_senha.click()
time.sleep(2)  # Aguarde o login ser processado

# 🔹 5. Ir para a página de atividades
url_atividades = "https://centralrelacionamento.sescsp.org.br/?path=lista-atividades"
driver.get(url_atividades)
time.sleep(3)

# Verificação
if "atividades" in driver.current_url:
    print("✅ Login realizado com sucesso e página de atividades carregada!")
else:
    print("❌ Erro ao logar no sistema.")

try:
    # 🔹 Lista de Unidades Selecionadas
    unidades_selecionadas = UNIDADES_SELECIONADAS

    caixa_procurar = driver.find_element(By.XPATH, "//input[@type='search']")
    caixa_procurar.send_keys("Ginástica Multifuncional")

    btn_procurar = driver.find_element(By.XPATH, "//button[@class='MuiButtonBase-root MuiIconButton-root']")
    btn_procurar.click()
    time.sleep(1) 
    
    # Selecionar categoria 'Esporte e Atividade física'
    categoria_esporte = driver.find_element(By.XPATH, "//li[contains(., 'Esporte e Atividade física')]")
    categoria_esporte.click()
    time.sleep(1)    

    # Publico geral
    if PUBLICO_GERAL : 
        publico_geral = driver.find_element(By.XPATH, "//li[contains(., 'Público em Geral')]")
        publico_geral.click()
        time.sleep(1)    

    for unidade in unidades_selecionadas:
        try:
            unidade = unidade.strip()
            elemento = driver.find_element(By.XPATH, f"//li[contains(., '{unidade}')]")
            elemento.click()
            print(f"✅ Selecionado: {unidade}")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Erro ao selecionar '{unidade}': {e}")

    # 🔹 Lista para armazenar unidades com inscrição aberta
    unidades_com_vagas = []

    # 🔹 Procurar por todas as atividades listadas na tabela
    atividades = driver.find_elements(By.XPATH, "//tr[@class='MuiTableRow-root']")

    for atividade in atividades:
        try:
            # Extrair o nome da unidade (ex: "Sesc Birigui", "Sesc Vila Mariana")
            unidade_element = atividade.find_element(By.XPATH, ".//div[contains(text(), 'Sesc')]")
            unidade = unidade_element.text.replace('Sesc','').strip()

            # Verificar se é uma unidade que estamos monitorando
            if any(u in unidade for u in unidades_selecionadas):
                # Procurar pelo botão "INSCREVER" dentro da atividade
                botao_inscrever = atividade.find_elements(By.XPATH, ".//span[contains(text(), 'Inscrever')]")
                
                if botao_inscrever:
                    unidades_com_vagas.append(unidade)                    

        except Exception as e:
            print(f"⚠ Erro ao verificar a atividade: {e}")

    # 🔹 Exibir Unidades com Inscrição Aberta
    if unidades_com_vagas:        
        message = "\n🔔 Unidades com inscrições abertas:"
        for unidade in unidades_com_vagas:
            message += f"\n- {unidade}"
        print(message)
        send_discord_message(message)    
    else:
        aviso = "\n❌ Nenhuma unidade selecionada tem inscrições abertas."
        print(aviso)        
        #send_discord_message(aviso)  
    
    print("\n")              

except Exception as e:
    print("Erro ao interagir com a página:", str(e))    

# Fechar o navegador
driver.quit()


