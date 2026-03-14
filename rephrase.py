import google.generativeai as genai
import os

# api_key = os.getenv("API_KEY")

genai.configure(api_key='AIzaSyBSFdHtnppuXaWcVCuEV4cTXl7kg5plnsI')
model = genai.GenerativeModel("gemini-1.5-flash")

def rephrase_text(text):
        
# Rephrase the text using the Google Generative AI API
    prompt = f'Rephrase this text to remove emotional language and make it neutral: "{text}"'
    response = model.generate_content(prompt)

    return response.text