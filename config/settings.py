from dotenv import load_dotenv
import os

# carrega o .env
load_dotenv()

# chaves
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

FOXBIT_KEY = os.getenv("FOXBIT_KEY")

FOXBIT_SECRET = os.getenv("FOXBIT_SECRET")