from langchain_groq import ChatGroq
from prompt.system_prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def saudacao():
    horario = int((datetime.now().strftime("%H")))
    if horario >= 6 and horario <= 12:
        return "Bom Dia!"
    elif horario > 12 and horario <= 17:
        return "Boa Tarde!"
    else:
        return "Boa Noite!"

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.5,
    max_tokens=2000
)

pergunta = input(f"Olá {saudacao()}, qual a sua duvida: ")

messages = [
    ( "system",SYSTEM_PROMPT,),
    ("human", pergunta),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)