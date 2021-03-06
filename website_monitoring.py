import requests
from bs4 import BeautifulSoup
import time
import smtplib
import re

articleDict = {}

fromaddr = 'biteen3d@gmail.com'
password = "28101998"
toaddrs  = ['vinzdruesne@gmail.com', 'vt.druesne@gmail.com']

url = "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie_puis_nblignes_est_200_puis_ordre_est_S_puis_sens_est_DESC_puis_f_est_58-10390,10709,10333,10278,11733,11575,11447,8743,10812,10851,8741,10586,10587,8742,11796.html"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def send_mail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def parse_article(article):
    name = article.find("h3").text
    id = article.find("section")["id"]
    status = article.find("section")["class"][0]
    link = "www.topachat.com" + article.find("a")["href"]
    price = article.find("div", "price").find("div", "prod_px_euro v16").text

    return (name, id, status, price, link)

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

for article in soup.find_all("article", class_="grille-produit NOR"):
    name, id, status, price, link = parse_article(article)
    articleDict[id] = {"name" : name, "status" : status, "price" : price, "link" : link}

print(articleDict)

while True:
    time.sleep(15)
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.find_all("article", class_="grille-produit NOR"):
            name, id, status, price, link = parse_article(article)

            if(id in articleDict):
                if(articleDict[id]["status"] != status):
                    send_mail("Subject: " + name + "\n\n" + status + " " + price[:-5] + "e " + link)
                    articleDict[id]["status"] = status
                    print(articleDict[id])
            else:
                send_mail("Subject: " + name + "\n\n" + status + " " + price[:-5] + "e " + link)
                articleDict[id] = {"name" : name, "status" : status, "price" : price, "link" : link}

    except Exception as e:
        send_mail("Subject: Error" + "\n\n" + str(e))
        print(e)
        continue
