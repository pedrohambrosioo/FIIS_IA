from selenium import webdriver
from selenium.webdriver.common.by import By
import json


navegador = webdriver.Chrome()#config do navegador
navegador.get("https://www.fundsexplorer.com.br")#acessando o site

links = navegador.find_elements(By.CSS_SELECTOR, "div.tab1 div.dataBox a")#/div tab1 / div dataBox / <a href>


dados = [
    {
        "nome": link.text.strip(),
        "url": link.get_attribute("href"),
        
    }
    for link in links 
]


# Salva no arquivo JSON
with open("fundos_links.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print("Arquivo JSON criado com sucesso!")







