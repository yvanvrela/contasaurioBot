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


# Iniciar al Menú Principal
def menu(bot, update):
  bot.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())


# Menus del bot
def main_menu(bot, update):
    bot.callback_query.message.edit_text(main_menu_message(),
                                         reply_markup=main_menu_keyboard())


def first_menu(bot, update):
    bot.callback_query.message.edit_text(first_menu_message(),
                                         reply_markup=first_menu_keyboard())


def second_menu(bot, update):
    bot.callback_query.message.edit_text(second_menu_message(),
                                         reply_markup=second_menu_keyboard())


def first_submenu(bot, update):
    pass


def second_submenu(bot, update):
    pass


def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Keyboardas - Menu de menues
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Configuración de Clientes', callback_data='m1')],
                [InlineKeyboardButton('Eliminar Cliente', callback_data='m2')],
                [InlineKeyboardButton('Opcion 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Nombre', callback_data='m1_1')],
                [InlineKeyboardButton('Timbrado', callback_data='m1_2')],
                [InlineKeyboardButton(
                    'Color de la Carpeta', callback_data='m1_3')],
                [InlineKeyboardButton('Atras', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


# Mensajes de los menus
def main_menu_message():
    return 'Opciones:'


def first_menu_message():
    return 'Editar Clientes:'


def second_menu_message():
    return 'Choose the submenu in second menu:'


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        allconfig['TOKEN'], use_context=True)

    dp = updater.dispatcher

    # los diferentes comandos para bot
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ayuda', help_command))

    dp.add_handler(CommandHandler('menu', menu))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Handlers del Menu
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_3'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_2'))
    updater.dispatcher.add_error_handler(error)


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
