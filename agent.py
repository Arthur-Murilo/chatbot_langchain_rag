from langchain_groq import ChatGroq
from prompt.system_prompt import PROMPT_2
from dotenv import load_dotenv

load_dotenv()



def inference(assunto: str):
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_tokens=1000
    )

    chain1 = PROMPT_2 | llm

    resposta = chain1.invoke({"tema": assunto})

    return resposta



assunto = input("Qual Tema do seu Twitter: ")
print(inference(assunto).content)

print("------------------------------------------------------------------")

print(inference("Surfer").content)