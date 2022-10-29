# pip freeze > requirements.txt
#* -- Importações
import os
import json
import telebot
import signal

#* -- Variáveis
TITLE = "TelegramBOT"
path = os.path.dirname(__file__) #? Caminho do diretório
token = json.load(open(f"{path}\\token.json"))["token"] #? Token do BOT
BOT = telebot.TeleBot(token)

#* -- Funções
def confirmExit(signum, frame):
    if input(f"\n[{TITLE}] Deseja realmente desligar o BOT? (s/n) ") == 's':
        print(f"[{TITLE}] BOT desligado.")
        exit(1)

def clearConsole() -> None: #? Limpa o console
    os.system("cls" if os.name == "nt" else "clear")

def detectChanges(messages):
	print(f"[{TITLE}#detectChanges] detected: {messages}")

#? Comando /ping
@BOT.message_handler(commands=["ping"])
def ping(message) -> None:
    print(f"\n[{TITLE}#ping] message: {message.text}")
    BOT.reply_to(message, "pong")

#? Responde sempre que receber uma mensagem
@BOT.message_handler(func=lambda message: True)
def spam(message) -> None:
    print(f"\n[{TITLE}#spam] message: {message.text}")
    BOT.reply_to(message, "spam")

#! Main
def main() -> None: #? Função principal
    signal.signal(signal.SIGINT, confirmExit)
    
    print(f"\n[{TITLE}] Iniciando o BOT...")
    
    BOT.set_update_listener(detectChanges)
    print(f"[{TITLE}] BOT iniciado.\n")
    # BOT.polling()
    BOT.infinity_polling()

if __name__ == "__main__":
    main()
