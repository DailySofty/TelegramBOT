# pip freeze > requirements.txt
# -- Importações
import os
import os.path as Path
import json

# -- Variáveis
path = Path.dirname(__file__) # Caminho do diretório
token = json.load(open(f'{path}\\..\\ignore\\token.json'))['token'] # Token
# Request GetMe

# -- Funções
def clearConsole() -> None: # Limpa o console
    os.system('cls' if os.name == 'nt' else 'clear')

def main() -> None:
    global token
    
    # --------------------------------------------------------------------------------------------------------------
    # 1 - Logar
    
    # 2 - Ler lista de chats
    chats = [] # Inicia uma lista vázia
    chats = "null" # Salva cada "chat" na lista "chats"
    print(f"\n{chats}")
    for chat in chats: # Laço que passa por cada "chat" dentro da lista "chats"
        print(f"{chat}")

    # 3 - Salvar apenas grupos (nome, data criada, criador, total participantes)

    # 4 - Ler mensagens de cada grupo

    # 5 - Identificar comandos

    # 6 - Executar comandos

    # 7 - Repetir etapa 2 até 6
    
    # 8 - Deslogar
    
    # 9 - Desligar BOT
    # --------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
