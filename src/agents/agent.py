import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain

from config.settings import settings
from config.prompts import SYSTEM_PROMPT
from loaders.document_loader import banco_qdrant


def get_session_history(session_id: str):
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=settings.MONGO_CONNECTION_STRING,
        database_name=settings.MONGO_DATABASE,
        collection_name=settings.MONGO_COLLECTION
    )


def criar_rag_chain():
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS
    )
    
    vector_store = banco_qdrant()
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    return retrieval_chain


def pergunta(assunto: str, session_id: str = "default") -> str:
    chain = criar_rag_chain()
    
    runnable_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )
    
    resposta = runnable_with_history.invoke(
        {"input": assunto},
        config={"configurable": {"session_id": session_id}}
    )
    
    return resposta["answer"]


if __name__ == "__main__":
    print("🏋️ Personal Trainer AI - RAG System\n")
    
    while True:
        duvida = input("💬 Qual sua dúvida? (ou 'sair' para encerrar): ")
        
        if duvida.lower() in ['sair', 'exit', 'quit']:
            print("👋 Até mais! Bons treinos!")
            break
        
        if not duvida.strip():
            continue
            
        print("\n⏳ Processando...\n")
        
        try:
            resposta = pergunta(duvida)
            print(f"🎯 Resposta:\n{resposta}\n")
        except Exception as e:
            print(f"❌ Erro: {str(e)}\n")
