import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import allconfig

# Iniciar Loggin
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# funcion para enviar el primer mensaje luego del /start


def start(update, context):
    """Mensaje de Inicio"""
    update.message.reply_text(
        'Que tengo que hacer? vea /ayuda para ver la lsita de mis funciones.')


# funcion para explicar los comandos, lista de opciones
def help_command(update, context):
    """Lista de Funciones"""
    update.message.reply_text(
        'Funciones para el control de los Clientes. \n\n /nuevocliente - agregar cliente \n /listaclientes - ver todos los clientes \n\n Configuración de Clientes \n /agregartimbrado - agregar un nuevo timbrado \n /recepciondocumentos - resive los documentos \n /retirodocumentos - nose \n /colorcarpeta - agregar el color \n\n Falta más funciones, pero aprendo rápido.')


def echo(update, context):
    # Busca una palabra clave, y responde con un mensaje
    update.message.reply_text("Entre en /ayuda para saber que hacer.")

# 
def menuSettings(update, context):
    update.message.reply_text("Entre en /ayuda para saber que hacer.")


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        allconfig['TOKEN'], use_context=True)

    dp = updater.dispatcher

    # los diferentes comandos para bot
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ayuda", help_command))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
