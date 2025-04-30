🎙️ Criador de Legendas com Tradução Automática

Este aplicativo permite transcrever arquivos de áudio ou vídeo e gerar legendas (.srt) automaticamente, com tradução para o português.
Ele utiliza modelos de Inteligência Artificial da OpenAI (Whisper) para transcrição e Argos Translate para tradução offline.

🔧 Funcionalidades
	•	📥 Upload de arquivos .mp3, .mp4, .wav, .m4a
	•	🔍 Detecção automática do idioma original
	•	📝 Geração de legendas no idioma original
	•	🌍 Tradução automática para português
	•	📤 Download das legendas nos formatos .srt
	•	🎧 Visualização de áudio ou vídeo no navegador
	•	📦 Tradução offline com pacotes do Argos Translate

💡 Tecnologias Utilizadas
	•	Python 3.10+
	•	Streamlit – Interface web
	•	Whisper (OpenAI) – Transcrição automática
	•	Argos Translate – Tradução offline
	•	Torch – Backend de inferência
	•	FFmpeg – Conversão e leitura de mídia

▶️ Como Executar

1. Clone o repositório

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

2. Instale as dependências

Recomenda-se usar um ambiente virtual.

pip install -r requirements.txt

3. Execute a aplicação

streamlit run app_legenda.py

A aplicação será iniciada em http://localhost:8501.

📁 Estrutura do Projeto

📦 seu-repositorio/
├── app_legenda.py           # Script principal da aplicação Streamlit
├── requirements.txt         # Dependências Python
├── packages.txt             # Dependências do sistema (ffmpeg)
└── .streamlit/
    └── config.toml          # Configuração opcional (se aplicável)

📌 Observações
	•	Os pacotes de tradução são baixados automaticamente na primeira execução.
	•	A tradução intermediária via inglês é usada se a tradução direta não estiver disponível.
	•	O Whisper requer uma GPU para melhor desempenho, mas funciona também em CPU com performance reduzida.

🛠️ Licença

Este projeto está licenciado sob os termos da MIT License.
