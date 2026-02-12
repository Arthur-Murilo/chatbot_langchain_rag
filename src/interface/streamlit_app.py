import streamlit as st
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent import pergunta


st.set_page_config(
    page_title="Personal Trainer AI",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        }
        
        .main-header {
            text-align: center;
            padding: 1.5rem 0;
            background: linear-gradient(90deg, #00ff88 0%, #00cc6a 100%);
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
        }
        
        .main-header h1 {
            color: #0a0a0a;
            font-weight: 800;
            margin: 0;
            font-size: 2.5rem;
        }
        
        .main-header p {
            color: #1a1a1a;
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        
        .user-message {
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            color: #0a0a0a;
            margin-left: 20%;
            box-shadow: 0 2px 10px rgba(0, 255, 136, 0.2);
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
            color: #00ff88;
            margin-right: 20%;
            border: 1px solid #00ff88;
            box-shadow: 0 2px 10px rgba(0, 255, 136, 0.1);
        }
        
        .message-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }
        
        .loading-dots {
            display: inline-block;
            animation: pulse 1.5s infinite;
        }
        
        .sidebar-content {
            background: #1a1a1a;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #00ff88;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #00ff88;
            margin: 0.5rem 0;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #00ff88;
        }
        
        .stat-label {
            color: #888;
            font-size: 0.9rem;
        }
        
        .stTextInput input {
            background: #2a2a2a;
            color: #00ff88;
            border: 2px solid #00ff88;
            border-radius: 10px;
            padding: 0.8rem;
        }
        
        .stTextInput input:focus {
            border-color: #00ff88;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
        }
        
        .stButton button {
            background: linear-gradient(90deg, #00ff88 0%, #00cc6a 100%);
            color: #0a0a0a;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 2rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton button:hover {
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
            transform: translateY(-2px);
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="main-header">
        <h1>🏋️ Personal Trainer AI</h1>
        <p>Seu assistente inteligente de treino e fitness</p>
    </div>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.message_count = 0


with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Configurações")
    
    session_id = st.text_input(
        "ID da Sessão",
        value="default",
        help="Identifique sua sessão para manter o histórico"
    )
    
    st.markdown("---")
    
    st.markdown("### 📊 Estatísticas")
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.message_count}</div>
            <div class="stat-label">Mensagens enviadas</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 💡 Dicas")
    st.info("""
    **Pergunte sobre:**
    - 🏋️ Exercícios e técnicas
    - 📋 Planejamento de treinos
    - 🥗 Nutrição e suplementos
    - 💊 Hábitos saudáveis
    - ⚡ Recuperação muscular
    """)
    
    st.markdown("---")
    
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <span class="message-icon">👤</span>
                    <strong>Você:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <span class="message-icon">🤖</span>
                    <strong>Personal Trainer AI:</strong><br>{message["content"]}
                </div>
            """, unsafe_allow_html=True)


st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Digite sua pergunta:",
        key="user_input",
        placeholder="Ex: Como fazer agachamento corretamente?",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("🚀 Enviar", use_container_width=True)


if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    
    with st.spinner(""):
        st.markdown("""
            <div class="chat-message assistant-message">
                <span class="message-icon">🤖</span>
                <strong>Personal Trainer AI:</strong><br>
                <span class="loading-dots">Pensando...</span>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.5)
        
        try:
            resposta = pergunta(user_input, session_id=session_id)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
            
        except Exception as e:
            error_msg = f"❌ Erro ao processar sua pergunta: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()


st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>💪 Desenvolvido com LangChain, Qdrant, Groq e Streamlit</p>
        <p style="font-size: 0.8rem;">🔒 Suas conversas são privadas e seguras</p>
    </div>
""", unsafe_allow_html=True)
