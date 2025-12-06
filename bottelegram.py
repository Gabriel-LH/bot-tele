
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import platform
import subprocess

TOKEN = os.getenv("BOT_TOKEN")

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = f"""
📟 *Sistema (Render):*
Python: {platform.python_version()}
Arquitectura: {platform.machine()}
    """
    await update.message.reply_text(info, parse_mode="Markdown")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("❗ Usa: /ping <host>")
    host = context.args[0]
    result = subprocess.getoutput(f"ping -c 4 {host}")
    await update.message.reply_text(f"📡 Ping:\n{result}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """
📜 *Comandos disponibles:*
/sysinfo - Info del sistema
/ping host - Prueba de ping
/help - Ayuda
"""
    await update.message.reply_text(texto, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("sysinfo", sysinfo))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("help", help_cmd))
    print("🤖 Bot corriendo desde Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
