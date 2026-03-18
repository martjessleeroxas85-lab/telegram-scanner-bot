from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

TOKEN = "8714402515:AAGib4B3n98twVwCnD8SeTcVL6_UWWoXtwc"
OWNER_ID = 6538213760

from telegram.ext import CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🤖 Welcome to Nexus File Safety Scanner

This bot scans Python files for:
• Malware behavior
• Token grabbers
• Suspicious code
• Hidden/obfuscated payloads

How to use:
1. Send a .py file
2. Wait for scan result
3. Check verdict (SAFE / DANGEROUS)

Send a file to begin.
"""
    await update.message.reply_text(msg)
    
async def scan_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document:
        await update.message.reply_text("Please send a .py file to scan.")
        return

    file = await document.get_file()
    filename = document.file_name

    path = f"temp_{filename}"
    await file.download_to_drive(path)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    if "exec(" in code or "eval(" in code:
        result = "⚠️ DANGEROUS"
    else:
        result = "✅ SAFE"

    user = update.message.from_user

    msg = f"""
📁 File Scanned
👤 User: {user.first_name}
🆔 ID: {user.id}
📄 File: {filename}
📊 Result: {result}
"""

    await update.message.reply_text(f"Scan result: {result}")
    await context.bot.send_message(chat_id=OWNER_ID, text=msg)

    os.remove(path)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))   # 👈 DITO
    app.add_handler(MessageHandler(filters.Document.ALL, scan_file))

    app.run_polling()
    
    app.add_handler(MessageHandler(filters.Document.ALL, scan_file))
    app.run_polling()


if __name__ == "__main__":
    main()