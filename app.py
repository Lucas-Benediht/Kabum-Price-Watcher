from bs4 import BeautifulSoup
import requests
import smtplib
import email.message
from dotenv import load_dotenv
import os
from colorama import Fore

load_dotenv()

# Url que será analisada 
URL = "https://www.kabum.com.br/produto/172365/memoria-kingston-fury-beast-8gb-3200mhz-ddr4-cl16-preto-kf432c16bb-8"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}

site = requests.get(URL, headers=headers)

soup = BeautifulSoup(site.content,'html.parser')

# Pegando o item 
title = soup.find('h1', class_ = 'sc-89bddf0f-6 dVrDvy').get_text().strip()

# Pegando o valor
price = soup.find('h4', class_ = 'finalPrice').get_text().strip()

# Convertendo para numérico 
num_price = price[3:8] 
num_price = num_price.replace(',', '')  # Remove os pontos da string
num_price = float(num_price) #Final da conversão

# Função de envio de e-mail
def send_email():
    email_content = """
    https://www.kabum.com.br/produto/172365/memoria-kingston-fury-beast-8gb-3200mhz-ddr4-cl16-preto-kf432c16bb-8
    """
    msg = email.message.Message()
    msg['Subject'] = 'Preço Memória RAM Baixou!!!'
    msg['From'] = 'lucasbenediht@gmail.com'
    msg['To'] = 'lucas_benediht@hotmail.com'
    password = os.getenv("EMAIL_PASSWORD")
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587) #Port do gmail
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
        print(Fore.MAGENTA + f"Sucesso ao enviar email")
    except Exception as e:
        print("Erro ao enviar email:", str(e))


if num_price < 2699:
    send_email()