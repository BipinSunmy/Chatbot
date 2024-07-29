from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts.chat import SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = GoogleGenerativeAI(model= "gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load(url):
    global embeddings
    data = YoutubeLoader.from_youtube_url(url)
    load = data.load()

    text = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    token = text.split_documents(load)
   
    ds = FAISS.from_documents(token,embeddings)
    return ds


def prompts(ds,prompt,):
    sim = ds.similarity_search(prompt)
    ans = " ".join([d.page_content for d in sim])
    llm = ChatGoogleGenerativeAI(model= "gemini-1.5-pro")
    template = """
        You are a chatbot who learns from the transcript and helps the user to learn it by giving answers to any question the user ask about the transcript:{docs}
        Only use the factual information from the transcript
        if you think that you don't have enough information regarding the question, say "i don't know"
        your answer shoild be verbose and detailed
    """
    system = SystemMessagePromptTemplate.from_template(template)
    hum_tem = "Answer the following question:{question}"
    human = HumanMessagePromptTemplate.from_template(hum_tem)
    chat_prompt = ChatPromptTemplate.from_messages([system,human])
    chain = LLMChain(llm=llm,prompt=chat_prompt)
    response = chain.run(question = prompt , docs = ans)
    response = response.replace("\n","")
    return response


def get_response(db,ques):
    response= prompts(ds=db,prompt=ques)
    return response
    