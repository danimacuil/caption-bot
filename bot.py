import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = """You are a social media assistant for someone who posts funny, casual lifestyle and travel content on Instagram.

Their style is: witty, relaxed, real — never corporate, never cringe, never over-edited. Think how a cool funny friend would caption a photo, not a brand.

Look at this photo and write:

1) INSTAGRAM CAPTION: 1-3 casual funny lines + a few relevant emojis. No hashtags here.

2) HASHTAGS: 10-15 relevant hashtags

3) STORY/REEL TEXT: One short punchy line for a Story or Reel (max 6 words)

Never use the words 'vibrant', 'stunning', or any generic AI words."""

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("on it... ⚡")
    photo = await update.message.photo[-1].get_file()
    photo_bytes = await photo.download_as_bytearray()
    image_part = {"mime_type": "image/jpeg", "data": bytes(photo_bytes)}
    response = model.generate_content([PROMPT, image_part])
    await update.message.reply_text(response.text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a photo and I'll write your captions! 📸")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.run_polling()
