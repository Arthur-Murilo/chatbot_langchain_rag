import os
from pathlib import Path
from typing import List
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import settings


def get_embeddings():
    return OllamaEmbeddings(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL
    )


def indexar_documentos(docs: List[Document]):
    QdrantVectorStore.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        url=settings.QDRANT_URL,
        collection_name=settings.QDRANT_COLLECTION
    )


def banco_qdrant():
    db = QdrantVectorStore.from_existing_collection(
        collection_name=settings.QDRANT_COLLECTION,
        url=settings.QDRANT_URL,
        embedding=get_embeddings()
    )
    return db


def carregar_documentos_pasta(pasta_path: str) -> List[Document]:
    documentos = []
    pasta = Path(pasta_path)
    
    for arquivo in pasta.iterdir():
        if not arquivo.is_file():
            continue
            
        print(f"📄 Carregando: {arquivo.name}")
        
        try:
            if arquivo.suffix == '.txt':
                loader = TextLoader(str(arquivo), encoding='utf-8')
                documentos.extend(loader.load())
            
            elif arquivo.suffix == '.pdf':
                loader = PyPDFLoader(str(arquivo))
                documentos.extend(loader.load())
            
            elif arquivo.suffix in ['.docx', '.doc']:
                loader = Docx2txtLoader(str(arquivo))
                documentos.extend(loader.load())
            
            else:
                print(f"⚠️  Formato não suportado: {arquivo.suffix}")
                continue
                
            print(f"✅ {arquivo.name} carregado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao carregar {arquivo.name}: {str(e)}")
    
    return documentos


if __name__ == '__main__':
    pasta_data = "data"
    
    print("🚀 Iniciando carregamento de documentos...\n")
    lista_documento_entrada = carregar_documentos_pasta(pasta_data)
    
    print(f"\n📊 Total de documentos carregados: {len(lista_documento_entrada)}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1000,
        chunk_overlap=200
    )
    documentos = text_splitter.split_documents(lista_documento_entrada)
    
    print(f"✂️  Total de chunks criados: {len(documentos)}")
    
    print("\n💾 Indexando documentos no Qdrant...")
    indexar_documentos(documentos)
    
    print("✅ Indexação concluída com sucesso! 🎉")
