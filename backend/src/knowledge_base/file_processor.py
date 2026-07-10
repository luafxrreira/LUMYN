from langchain_text_splitters import CharacterTextSplitter
# from PyPDF2 import PdfReader
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
my_text = os.path.join(BASE_DIR, "about_lumyn.txt")

def process_files(files=None):
    my_text = "src/knowledge_base/about_lumyn.txt"
    try:
        with open(my_text, 'r', encoding='utf-8') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {my_text}")
        return ""
    except Exception as e:
        print(f"Erro ao ler o arquivo {my_text}: {e}")
        return ""

def create_text_chunks(my_text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=300,
        chunk_overlap=50,
        length_function=len
    )

    chunks = text_splitter.split_text(my_text)
    return chunks