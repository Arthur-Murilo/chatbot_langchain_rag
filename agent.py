from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from prompt.system_prompt import SYSTEM_PROMPT
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


def get_session_history(session_id: str):
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://admin:admin@localhost:27017",  # sua conexão MongoDB
        database_name="chat_history",
        collection_name="message_store"
    )

def pergunta(assunto: str):
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_tokens=1000
    )

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{assunto}"),
    ]
)

    chain1 = prompt | llm | StrOutputParser()

    runnable_with_history = RunnableWithMessageHistory(  
    chain1,  
    get_session_history  
)  

    resposta = runnable_with_history.invoke(
        {"human": assunto},  # ← FALTOU O INPUT!
        config={"configurable": {"session_id": "1"}}
    )

    return resposta



if __name__ == "__main__":
    duvida = input("Qual sua duvida?: ")
    print(pergunta(duvida))