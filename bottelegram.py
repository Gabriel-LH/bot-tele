import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import platform
import subprocess


PORT = int(os.environ.get('PORT', '8080'))


WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_HOSTNAME') 
WEBHOOK_PATH = os.environ.get('TOKEN', '/secretpath') # Usaremos el token o un path secreto para el endpoint

TOKEN = os.getenv("BOT_TOKEN")

# --- Funciones de Comandos (Sin cambios) ---

async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info = f"""
📟 <b>Sistema (Render):</b>
Python: {platform.python_version()}
Arquitectura: {platform.machine()}
    """
    await update.message.reply_text(info, parse_mode="HTML") # Cambiar a HTML

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("❗ Usa: /ping <host>")
    host = context.args[0]
    # Usamos '-c 4' para 4 intentos de ping (funciona en Linux/Render)
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

# --- Función Main con Webhook ---

def main():
    if not TOKEN:
        print("❌ Error: No se encontró la variable de entorno BOT_TOKEN.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    # Añadir los manejadores de comandos
    app.add_handler(CommandHandler("sysinfo", sysinfo))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("help", help_cmd))

    print(f"🤖 Configurando Webhook en: https://{WEBHOOK_URL}{WEBHOOK_PATH}")

    # 2. Iniciar el servidor web para escuchar peticiones de Telegram
    app.run_webhook(
        listen="0.0.0.0", # Escuchar en todas las interfaces de red (necesario en Render)
        port=PORT,
        webhook_url=f'https://{WEBHOOK_URL}{WEBHOOK_PATH}',
        url_path=WEBHOOK_PATH # El path donde el bot espera las llamadas de Telegram
    )

if __name__ == "__main__":
    main()