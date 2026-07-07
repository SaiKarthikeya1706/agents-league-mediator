import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
for m in genai.list_models():
    print(m.name, "->", m.supported_generation_methods)