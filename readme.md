# Chat CLI com LLM (OpenRouter API)

Um chatbot de linha de comando que se conecta a um modelo de linguagem (LLM) via API da OpenRouter, mantendo o histórico da conversa para gerar respostas com contexto.

## Objetivo

Projeto criado para aplicar na prática conceitos de integração com LLMs: chamadas de API, gerenciamento de histórico de conversa (contexto), e tratamento de erros de rede/API — a base necessária antes de evoluir para técnicas mais avançadas como RAG e prompt engineering estruturado.

## Funcionalidades

- Conversa contínua com um modelo de LLM via terminal
- Histórico de mensagens mantido em memória e enviado a cada requisição, para que o modelo tenha contexto das perguntas anteriores
- Comando `histórico` para visualizar as mensagens trocadas até o momento
- Comando `sair` para encerrar a conversa
- Tratamento de erros de conexão (rede) e de resposta da API (status code diferente de 200), removendo do histórico mensagens que não obtiveram resposta válida, para manter o contexto consistente

## Tecnologias utilizadas

- Python
- [Requests](https://docs.python-requests.org/) — chamadas HTTP
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente
- [OpenRouter API](https://openrouter.ai/) — acesso a modelos de LLM

## Como rodar

1. Clone o repositório
2. Instale as dependências em um ambiente virtual:
   ```bash
   (venv) pip install requests python-dotenv
   ```
3. Copie o arquivo `.env.example` para `.env` e adicione sua chave de API:
   ```bash
   cp .env.example .env
   ```
   ```
   API_KEY=sua_chave_aqui
   ```
4. Execute o script:
   ```bash
   python ai-study/chat.py
   ```

## Comandos disponíveis durante a conversa

| Comando | Ação |
|---|---|
| `sair` | Encerra o chat |
| `historico` | Exibe todas as mensagens trocadas até o momento |
| qualquer outro texto | Envia a pergunta ao modelo |