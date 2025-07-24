from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import mysql.connector
import datetime

def call_best_Wrost_of_day():#funcao para exibir os fundos com ALTA
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="fiis_db"
) 
    cursor = conexao.cursor()
    today = datetime.date.today()#pega a data de hoje
    
    navegador = webdriver.Chrome()#config do navegador
    navegador.get("https://www.fundsexplorer.com.br")#acessando o site
    links = navegador.find_elements(By.CSS_SELECTOR, "div.tab1 div.dataBox")#/div tab1 / div dataBox
    dados = []
    for item in links:
        try:
            nome = item.find_element(By.TAG_NAME, "a").text.strip()# procura o nome do fundo
            url = item.find_element(By.TAG_NAME, "a").get_attribute("href")# URL
            variacao = item.find_element(By.CLASS_NAME, "alta").text.strip()# variacao do fundo %
            dados.append((nome,url,variacao,today))
        except Exception as e:
            print("Erro ao processar item:", e)
    links_pior = navegador.find_elements(By.CSS_SELECTOR, "div.tab2 div.dataBox")#/div tab2 / div dataBox

    
    
    for item in links_pior:
        try:
            nome = item.find_element(By.TAG_NAME, "a").text.strip()# procura o nome do fundo
            url = item.find_element(By.TAG_NAME, "a").get_attribute("href")# URL
            variacao = item.find_element(By.CLASS_NAME, "baixa").text.strip()# variacao do fundo %
            dados.append((nome,url,"-"+variacao,today))
        except Exception as e:
            print("Erro ao processar item:", e)
    # Verifica se já existem registros para hoje
    cursor.execute("SELECT COUNT(*) FROM fundos WHERE data_consulta = %s", (today,))
    (count,) = cursor.fetchone()
    if count > 0:
        print("Já existem registros gravados para hoje. Não será feita nova gravação.")
    else:
        sql = "INSERT INTO fundos (nome, url, variacao, data_consulta) VALUES (%s, %s, %s, %s)"
        cursor.executemany(sql, dados)
        conexao.commit()
        print(f"{cursor.rowcount} registros inseridos com sucesso!")
    cursor.close()
    conexao.close()
    navegador.quit()









