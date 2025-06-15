import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import time

# Configuração inicial
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def chat(prompt, message_history):
    system_message = """Você é o TEA Helpbot, tutor especializado em matemática para alunos autistas. Siga EXATAMENTE:

    **ESTILO ORIGINAL:**
    1. Comece validando: "Tudo bem! Vamos revisar juntos"
    2. Use linguagem mediadora:
       - "Para isolar o x" (não "resolver a equação")
       - "O que acontece quando..." (não "subtraia")
    3. Termine com pergunta aberta
    4. Validação em 2 etapas:
       a) Confirmação do passo atual
       b) Pergunta para o próximo passo

    **EXEMPLO PARA 3x + 5 = 17:**
    Usuário: "3x + 5 = 17, não sei"
    Assistente: "Tudo bem! Vamos revisar juntos. Para isolar o x, precisamos eliminar o +5. O que acontece quando movemos o 5 para o outro lado?"
    """

    messages = [
        {"role": "system", "content": system_message},
        *message_history[-3:],
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2,
        max_tokens=80,
        stop=["\n"]  # Para respostas mais curtas
    )
    return response.choices[0].message.content

# Interface (mantida igual)
def stream(text):
    full_response = ""
    placeholder = st.empty()
    for char in text:
        full_response += char
        placeholder.markdown(full_response)
        time.sleep(0.03)
    return full_response

st.set_page_config(
    page_title="TEA Helpbot Original",
    page_icon="🧮",
    layout="centered"
)

st.title("🤖 TEA Helpbot (Modo Original)")
st.caption("Tutor de Matemática - Fundamental II")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Qual equação vamos resolver juntos hoje?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Digite sua equação..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        resposta = stream(chat(user_input, st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": resposta})
