Descrição

Este projeto utiliza visão computacional para reconhecer um tabuleiro de xadrez a partir de uma imagem e mapear as peças para um tabuleiro virtual. O sistema é composto por um backend em Python com Flask e um modelo YOLOv5 treinado para detecção de tabuleiros e peças, e um frontend desenvolvido em Vue.js para visualização interativa.

Requisitos

- Python 3.8
- Flask (para o backend)
- YOLOv5 (modelo de detecção de peças e tabuleiro)
- Node.js e npm (para rodar o frontend Vue.js)
- Sistema operacional Linux (Ubuntu recomendado)

Como Rodar o Projeto

1. Configuração Inicial

Antes de rodar o projeto, altere os IPs no backend e frontend conforme o IP da sua máquina:

# No frontend: Modifique o arquivo vue.config.js

2. Rodando o Backend

Execute os seguintes comandos no terminal:

cd backend
FLASK_APP=app.py flask run --host=0.0.0.0 --port=8000

Isso iniciará o servidor Flask e disponibilizará a API do modelo YOLOv5.

3. Rodando o Frontend

Em outro terminal, execute:

cd frontend
npm install  # Instala as dependências do projeto (somente na primeira execução)
npm run serve

Isso iniciará o frontend Vue.js, permitindo que você carregue uma imagem do tabuleiro e visualize a detecção.

Funcionamento

O frontend permite ao usuário carregar uma imagem do tabuleiro de xadrez.

Ao clicar em Detectar Peças, a imagem é enviada para o backend.

O backend utiliza o modelo YOLOv5 para reconhecer o tabuleiro e as peças.

As coordenadas das peças detectadas são enviadas de volta ao frontend.

O frontend exibe um tabuleiro virtual ao lado da imagem original, refletindo a posição das peças detectadas.

Tecnologias Utilizadas

- Flask para criar a API do backend
- YOLOv5 para detecção do tabuleiro e peças
- Vue.js para o frontend
- Node.js/NPM para gerenciar dependências do frontend

Considerações Finais

- O projeto foi desenvolvido para ser executado no Linux (Ubuntu recomendado).
- Certifique-se de que os IPs no config.py e vue.config.js estejam corretos antes de rodar o sistema.
- Caso haja algum problema de dependência, reinstale os pacotes necessários com:
  pip install -r requirements.txt (no backend)
  npm install (no frontend)
