import os
import telebot
import spacy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('BOT')
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Load the spaCy model only once
nlp = spacy.load("en_core_web_sm")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "Howdy, how are you doing?\nHalo halo, coba doang ini."
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['resume'])
def resume_text_spacy(message):
    # Extract the text following the command
    if not message.text.strip().split(" ", 1)[1:]:
        bot.reply_to(message, "Silakan berikan teks setelah perintah /resume")
        return

    teks = message.text.strip().split(" ", 1)[1]  # Get text after the command
    kalimat_count = 2  # Number of sentences to include in the resume

    # Process the text with spaCy
    doc = nlp(teks)
    kalimat = [sent.text for sent in doc.sents]
    resume = ' '.join(kalimat[:kalimat_count])

    # Send the resume back to the user
    bot.reply_to(message, f"Your Resume:\n{resume}\n")
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start polling for updates
bot.infinity_polling()