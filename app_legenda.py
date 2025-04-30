import streamlit as st
import whisper
import tempfile
import os
from pathlib import Path
from argostranslate import translate

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def carregar_tradutor(origem, destino):
    idiomas = translate.get_installed_languages()
    lang_origem = next((l for l in idiomas if l.code == origem), None)
    lang_destino = next((l for l in idiomas if l.code == destino), None)
    if lang_origem and lang_destino:
        return lang_origem.get_translation(lang_destino)
    return None

def traduzir_texto(texto, idioma_origem):
    if idioma_origem in ["pt", "pb"]:
        return texto
    tradutor = carregar_tradutor(idioma_origem, "pt") or carregar_tradutor(idioma_origem, "pb")
    if tradutor:
        try:
            return tradutor.translate(texto)
        except:
            return texto
    else:
        tradutor_inter = carregar_tradutor(idioma_origem, "en")
        tradutor_final = carregar_tradutor("en", "pt") or carregar_tradutor("en", "pb")
        if tradutor_inter and tradutor_final:
            try:
                texto_inter = tradutor_inter.translate(texto)
                return tradutor_final.translate(texto_inter)
            except:
                return texto
        else:
            return texto

def gerar_srt(segments, traduzido=False, idioma_origem="en"):
    srt = ""
    for i, seg in enumerate(segments):
        inicio = format_time(seg["start"])
        fim = format_time(seg["end"])
        texto = seg["text"].strip()
        if traduzido:
            texto = traduzir_texto(texto, idioma_origem)
        srt += f"{i + 1}\n{inicio} --> {fim}\n{texto}\n\n"
    return srt

st.title("🗣️ Transcrição e Tradução Online com Legendas")

uploaded_file = st.file_uploader("Envie seu arquivo de áudio ou vídeo", type=["mp3", "mp4", "wav", "m4a"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    st.subheader("🎧 Reproduzir Arquivo")
    if uploaded_file.type.startswith("audio"):
        st.audio(temp_path)
    else:
        st.video(temp_path)

    st.subheader("🔁 Transcrevendo...")
    model = whisper.load_model("medium")
    resultado = model.transcribe(temp_path)
    idioma_detectado = resultado.get("language", "auto")

    idiomas = translate.get_installed_languages()
    idioma_nome = next((l.name for l in idiomas if l.code == idioma_detectado), idioma_detectado)
    st.success(f"Idioma detectado: {idioma_detectado.upper()} - {idioma_nome}")

    srt_original = gerar_srt(resultado["segments"], traduzido=False)
    srt_traduzido = gerar_srt(resultado["segments"], traduzido=True, idioma_origem=idioma_detectado)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 Transcrição")
        st.text_area("Texto Original", value=srt_original, height=400, key="orig")

    with col2:
        st.subheader("🌍 Tradução Português")
        st.text_area("Texto Traduzido", value=srt_traduzido, height=400, key="trad")

    st.subheader("📥 Baixar Legendas")
    st.download_button("Baixar SRT Original", srt_original, file_name="original.srt")
    st.download_button("Baixar SRT Traduzido", srt_traduzido, file_name="traduzido.srt")
