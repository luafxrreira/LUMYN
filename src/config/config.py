import os
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)

def get_api_key():
    API_KEY = os.getenv("API_KEY")

    print(f"\nProcurando .env em: {env_path}")
    print(f"API_KEY carregada: {API_KEY is not None}")

    return API_KEY