import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
from PIL import Image
import io
import os



def scraping(deck_code="kVVF5w-bueC8Z-FFVvkF", driver_dir):
    # deck_code = "kVVF5w-bueC8Z-FFVvkF/"
    options = Options()
    options.set_headless(True)

    load_url = "https://www.pokemon-card.com/deck/confirm.html/deckID/" + str(deck_code) + "/"
    driver = webdriver.Chrome(chrome_options=options,executable_path=driver_dir)
    driver.get(load_url)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    os.makedirs("pokeca_img", exist_ok=True)
    # URLからデッキを読み込む
    deck = {}
    deck_list = []
    deck_img = {}
    base_url = "https://www.pokemon-card.com"
    for i in range(1,5):
        for j in range(1,16):
            try:
                # カードの名前と枚数を取得
                card = soup.select("#cardImagesView > div:nth-child("+str(j)+") > div:nth-child("+ str(i) +") > table > tbody > tr.imgBlockArea > td > a")[0].img["alt"]
                num =  int(soup.select("#cardImagesView > div:nth-child("+str(j)+") > div:nth-child("+ str(i) +") > table > tbody > tr:nth-child(2) > td > span")[0].text[0])
                # カードのタイプを取得 P->ポケモン T->トレーナーズ E->エネルギー
                type_ = soup.select("#cardImagesView > div:nth-child("+str(j)+") > div:nth-child("+ str(i) +") > table > tbody > tr.imgBlockArea > td > a")[0].img["src"].split("/")[6].split("_")[1]
                for _ in range(num):
                    deck_list.append(card)
                deck[card] = [num,type_]
                img_url = base_url + soup.select("#cardImagesView > div:nth-child("+str(j)+") > div:nth-child("+ str(i) +") > table > tbody > tr.imgBlockArea > td > a")[0].img["src"]
                img = Image.open(io.BytesIO(requests.get(img_url).content))
                img_name = "pokeca_img/img_{}.png".format(card)
                if not os.path.isdir(img_name):
                    plt.figure(figsize=(1,1))
                    plt.axis("off")
                    plt.imshow(img)
                    plt.savefig(img_name, bbox_inches="tight", pad_inches=0.0)
                deck_img[card] = img_name
            except:
                continue
    
    return deck, deck_list, deck_img
