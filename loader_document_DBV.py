import os
from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings


def get_embeddings():
    """Retorna os embeddings do Ollama"""
    return OllamaEmbeddings(model="nomic-embed-text")


def indexar_documentos(docs: list):
    """Indexa documentos no Qdrant"""
    QdrantVectorStore.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        url="http://localhost:6333",
        collection_name="rag_gym_personal"
    )


def banco_qdrant():
    """Conecta ao banco Qdrant existente"""
    db = QdrantVectorStore.from_existing_collection(
        collection_name="rag_gym_personal",
        url="http://localhost:6333",
        embedding=get_embeddings()
    )
    return db


def carregar_documentos_pasta(pasta_path: str):
    """Carrega todos os arquivos .txt da pasta especificada"""
    documentos = []
    pasta = Path(pasta_path)
    
    for arquivo in pasta.glob("*.txt"):
        print(f"Carregando: {arquivo.name}")
        loader = TextLoader(str(arquivo), encoding='utf-8')
        documentos.extend(loader.load())
    
    return documentos


if __name__ == '__main__':
    # Carrega todos os arquivos da pasta data
    pasta_data = "data"
    lista_documento_entrada = carregar_documentos_pasta(pasta_data)
    
    print(f"Total de documentos carregados: {len(lista_documento_entrada)}")
    
    # Criando os Chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200
    )
    documentos = text_splitter.split_documents(lista_documento_entrada)
    
    print(f"Total de chunks criados: {len(documentos)}")
    
    # Indexando os documentos
    print("Indexando documentos no Qdrant...")
    indexar_documentos(documentos)
    
    print("Indexação concluída com sucesso!")