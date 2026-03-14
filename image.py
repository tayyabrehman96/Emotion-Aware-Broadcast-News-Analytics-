import google.generativeai as genai
from PIL import Image
import httpx
import os
import base64

# Configure the API key
genai.configure(api_key='AIzaSyBSFdHtnppuXaWcVCuEV4cTXl7kg5plnsI')

# Define the model
model = genai.GenerativeModel("gemini-1.5-flash")

image_path = "https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvam9iNjc5LTEwMy14LmpwZw.jpg"

image = httpx.get(image_path)

prompt = "Caption this image."
response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])

print(response.text)
