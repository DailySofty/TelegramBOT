# pip freeze > requirements.txt
#* -- Importações
import json
import os
import signal
import telebot
from bs4 import BeautifulSoup
import requests
import json
import base64

#* -- Variáveis
TITLE = "TelegramBOT"
PATH = os.path.dirname(__file__)  #? Caminho do diretório
TOKEN = json.load(open(f"{PATH}\\token.json"))["token"]  #? Token do BOT
DATA = []
BOT = telebot.TeleBot(TOKEN)

#* -- Funções
def confirmExit(signum, frame) -> None:
    if input(f"\n[{TITLE}] Deseja realmente desligar o BOT? (s/n) ") == 's':
        print(f"[{TITLE}] BOT desligado.")
        exit(1)

def clearConsole() -> None:  #? Limpa o console
    os.system("cls" if os.name == "nt" else "clear")

def getData(mode) -> None:
    global DATA
    
    DATA = []
    
    match mode:
        case "top100":
            url = requests.get('https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating')

            soup = BeautifulSoup(url.content, 'html.parser')

            filmes = soup.findAll('div', {'class': 'lister-item mode-advanced'})

            for filme in filmes:
                titulo = (filme.h3.a.text)
                ano = (filme.find('span', {'class': 'lister-item-year text-muted unbold'}).text[1:5])
                nota = (filme.find('div', {'class': 'inline-block ratings-imdb-rating'})['data-value'])
                imagem = (filme.find('img', {'class': 'loadlate'})['loadlate'])

                DATA.append({
                    'titulo': titulo,
                    'imagem': imagem,
                    'ano': ano,
                    'nota': nota
                })

        case "popular":
            url = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=watch_tpks_chtmvm')

            soup = BeautifulSoup(url.content, 'html.parser')

            filmes = soup.find('tbody', {'class': 'lister-list'}).findAll('tr')
            
            print(f"[{TITLE}#getData] filmes: {filmes}")

            for filme in filmes:
                titulo = filme.find('td', {'class': 'titleColumn'}).a.text
                
                ano = filme.find('span', {'class': 'secondaryInfo'}).text.replace("(", "").replace(")", "")
                nota = filme.find('td', {'class': 'imdbRating'}).text.replace("\n", "")
                imagem = filme.find('td', {'class': 'posterColumn'}).img.src

                DATA.append({
                    'titulo': titulo,
                    'imagem': imagem,
                    'ano': ano,
                    'nota': nota
                })
        case _: 
            url = requests.get('https://www.imdb.com/chart/moviemeter/?ref_=watch_tpks_chtmvm')

            soup = BeautifulSoup(url.content, 'html.parser')

            filmes = soup.find('tbody', {'class': 'lister-list'}).findAll('tr')
            
            print(f"[{TITLE}#getData] filmes: {filmes}")

            for filme in filmes:
                titulo = filme.find('td', {'class': 'titleColumn'}).a.text
                
                ano = filme.find('span', {'class': 'secondaryInfo'}).text.replace("(", "").replace(")", "")
                nota = filme.find('td', {'class': 'imdbRating'}).text.replace("\n", "")
                imagem = filme.find('td', {'class': 'posterColumn'}).img.src

                DATA.append({
                    'titulo': titulo,
                    'imagem': imagem,
                    'ano': ano,
                    'nota': nota
                })
    
    print(f"[{TITLE}#getData] DATA: {DATA}")

def convertImg(url) -> str:
    print(f"[{TITLE}#convertImg] url: {url}")
    
    imgRes = requests.get(url).content
    print(f"[{TITLE}#convertImg] imgRes: {imgRes}")
    
    img64 = base64.b64encode(imgRes)
    print(f"[{TITLE}#convertImg] img64: {img64}")
    return img64

def detectChanges(messages) -> None:
    print(f"[{TITLE}#detectChanges] detected: {messages}")

#? Comando /ping
@BOT.message_handler(commands=["ping"])
def ping(message) -> None:
    print(f"\n[{TITLE}#ping] message: {message.text}")
    BOT.reply_to(message, "pong")
    print(DATA)

#? Comando /filmes
@BOT.message_handler(commands=["filmes"])
def filmes(message) -> None:
    print(f"\n[{TITLE}#filmes] message: {message.text}")
    
    try:
        mode = message.text.split()[1:][0]
    except:
        mode = None
    
    print(f"\n[{TITLE}#filmes] mode: {mode}")
    
    getData(mode)
    
    filmesMsg_part1 = "Filmes:"
    filmesMsg_part2 = ""
    
    for index, filme in enumerate(DATA):
        # filmesLine = f"`{index + 1}` {filme['titulo']} _({filme['ano']})_ - *{filme['nota']}*"
        # filmesLine = f"<code>{index + 1}</code> <b>{filme['titulo']}</b> <i>({filme['ano']})</i> - ⭐️ <b>{filme['nota']}</b>"
        filmesLine = f"<code>{index + 1}</code> <b>{filme['titulo']}</b> ({filme['ano']}) - ⭐️ {filme['nota']}"
        print(f"\n[{TITLE}#filmes] filmesLine: {filmesLine}")
        
        if ((index + 1) < 51):            
            filmesMsg_part1 += f"\n\n{filmesLine}"
        else:
            filmesMsg_part2 += f"\n\n{filmesLine}"
        # BOT.send_photo(message, photo=open(convertImg(filme['imagem']), 'rb')) #! Não funciona com imagem
    
    print(f"\n[{TITLE}#filmes] filmesMsg: {filmesMsg_part1 + filmesMsg_part2}")
    BOT.reply_to(message, filmesMsg_part1, parse_mode='HTML')
    BOT.reply_to(message, filmesMsg_part2, parse_mode='HTML')

#? Responde sempre que receber uma mensagem
@BOT.message_handler(func=lambda message: True)
def spam(message) -> None:
    print(f"\n[{TITLE}#spam] message: {message.text}")
    BOT.reply_to(message, "spam")

#! Main
def main() -> None:  #? Função principal    
    # signal.signal(signal.SIGINT, confirmExit)
    # signal.signal(signal.SIGQUIT, confirmExit)
    signal.signal(signal.SIGTERM, confirmExit)

    print(f"\n[{TITLE}] Iniciando o BOT...")

    BOT.set_update_listener(detectChanges)
    print(f"[{TITLE}] BOT iniciado.\n")
    BOT.polling()
    # BOT.infinity_polling()

if __name__ == "__main__":
    main()
