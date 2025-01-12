import google.generativeai as genai
from googletrans import Translator

translator = Translator()

genai.configure(api_key="AIzaSyA4sN6DC8ssBsFgQULCxXbZjpB5AMALXMQ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")

text = response.text

translated = translator.translate(text, src="en", dest="pt")

print(translated.text)