# pip freeze > requirements.txt
#* -- Importações
import os
import json
import time
import requests

#* -- Variáveis
path = os.path.dirname(__file__) #? Caminho do diretório
api_url = "https://api.telegram.org/bot" #? URL da API do Telegram
token = json.load(open(f"{path}\\..\\ignore\\token.json"))["token"] #? Token do BOT

#* -- Classes
class Bot:
    global api_url, token #? Definir variáveis como globais
    def __init__(self) -> None: #? Instanciar o BOT
        self.base_url = api_url + token
    
    def run(self) -> None: #? Executar BOT
        update_id = None
        
        while True:
            print("Buscando mensagens...\n")
            update = self.getUpdates(update_id)
            if messages := update["result"]:
                print(f"/ Mensagens encontradas: {len(messages)}\n|")
                for message in messages:
                    if "message" in message:
                        print(f"| Enviando mensagem #{list(messages).index(message) + 1}...")
                        update_id = message["update_id"]
                        chat_id = message["message"]["from"]["id"]
                        reply = self.createReply()
                        self.sendMessage(reply, chat_id)
                        print(f"| Mensagem #{list(messages).index(message) + 1} enviada!\n|")
                print("\ Todas mensagens foram respondidas!\n")
            else:
                print("Nenhuma mensagem encontrada...\n")
    
    def getUpdates(self, update_id) -> dict: #? Ler atualizações
        getUpdates_url = f"{self.base_url}/getUpdates?timeout=10" #? timeout: Verifica a cada 2 minutos (120s)
        
        if update_id:
            getUpdates_url = f"{getUpdates_url}&offset={update_id + 1}" #? update_id + 1: Pega a mensagem mais recente
        
        result = requests.get(getUpdates_url)
        
        return json.loads(result.content)
    
    def createReply(self) -> str: #? Retornar resposta
        return "1st reply"
    
    def sendMessage(self, reply, chat_id) -> None: #? Enviar mensagem
        sendMessage_url = f"{self.base_url}/sendMessage?chat_id={chat_id}&text={reply}"
        requests.get(sendMessage_url)
    
    #TODO Salvar apenas grupos (nome, data criada, criador, total participantes)

    #TODO Ler mensagens de cada grupo

    #TODO Identificar comandos
    
    #TODO Executar comandos

#* -- Funções
def clearConsole() -> None: #? Limpa o console
    os.system("cls" if os.name == "nt" else "clear")

def main() -> None:
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
