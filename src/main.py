# pip freeze > requirements.txt
# * -- Importações
import os
import json
import telebot
import signal

# * -- Variáveis
path = os.path.dirname(__file__)  # ? Caminho do diretório
token = json.load(open(f"{path}\\token.json"))["token"]  # ? Token do BOT
BOT = telebot.TeleBot(token)

# * -- Funções
def main() -> None:  # ? Função principal
    signal.signal(signal.SIGINT, confirmExit)
    
    print("Iniciando o BOT...")
    BOT.polling()

def confirmExit(signum, frame):
    if input("\nDeseja realmente desligar o BOT? (s/n)\n>>> ") == 's':
        exit(1)

def clearConsole() -> None:  # ? Limpa o console
    os.system("cls" if os.name == "nt" else "clear")

def returnTrue(message) -> bool:  # ? Retorna True
    return True

@BOT.message_handler(func=returnTrue)  # ? Responde sempre que receber uma mensagem
def spam(message) -> None:
    BOT.reply_to(message, "spam")

@BOT.message_handler(commands=["test"])  # ? Comando /test
def test(message) -> None:  # ? Responde a mensagem
    BOT.reply_to(message, "Testado!")

#! Main
if __name__ == "__main__":
    main()
