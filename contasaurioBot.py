import logging
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import allconfig
from export_files import xls_to_txt, scan_files, read_file, write_file, to_zip, delete_file


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
        'Funciones para el control de los Clientes. \n\n /nuevocliente - agregar cliente \n /listaclientes - ver todos los clientes \n\n Configuración de Clientes \n /agregartimbrado - agregar un nuevo timbrado \n /recepciondocumentos - resive los documentos \n /retirodocumentos - nose \n /colorcarpeta - agregar el color \n /export - exportar archivos de la R-90 \n\n Falta más funciones, pero aprendo rápido.')


def echo(update, context):
    # Busca una palabra clave, y responde con un mensaje
    update.message.reply_text("Entre en /ayuda para saber que hacer.")


def export_files(update, context):

    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id, text='Exportando archivos...')

    xls_to_txt()

    files = scan_files()

    if files:

        context.bot.send_message(
            chat_id=chat_id, text='Encontré estos archivos: ')

        for file in files:
            file_name = re.findall('\w+.txt', file)
            name = file_name[0]
            context.bot.send_message(
                chat_id=chat_id, text=name.replace('.txt', '.xls'))

        for file in files:

            file_content = read_file(file)

            write_file(file_content, path=file)

            to_zip(file)

            delete_file(file)

        context.bot.send_message(
            chat_id=chat_id, text='Formateando los archivos y exportando a zip...')

        context.bot.send_message(
            chat_id=chat_id, text='Lestoo, yia terminé :)')

    else:
        context.bot.send_message(
            chat_id=chat_id, text='No hay archivos nuevos :(')

# Iniciar al Menú Principal


def menu(bot, update):
    bot.message.reply_text(mainMenuMessage(),
                           reply_markup=mainMenuKeyboard())


# Menus del bot
def mainMenu(bot, update):
    bot.callback_query.message.edit_text(mainMenuMessage(),
                                         reply_markup=mainMenuKeyboard())


def clientConfigMenu(bot, update):
    bot.callback_query.message.edit_text(clientConfigMessage(),
                                         reply_markup=clientConfigKeyboard())


def second_menu(bot, update):
    bot.callback_query.message.edit_text(second_menu_message(),
                                         reply_markup=second_menu_keyboard())


def clientConfigSubmenu(bot, update):
    pass


def second_submenu(bot, update):
    pass


def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Keyboardas - Menu de menues
def mainMenuKeyboard():
    keyboard = [[InlineKeyboardButton('Configuración de Clientes', callback_data='clientConfigMenu')],
                [InlineKeyboardButton('Eliminar Cliente', callback_data='m2')],
                [InlineKeyboardButton('Opcion 3', callback_data='m3')]]
    return InlineKeyboardMarkup(keyboard)


def clientConfigKeyboard():
    keyboard = [[InlineKeyboardButton('Nombre', callback_data='clientName')],
                [InlineKeyboardButton(
                    'Timbrado', callback_data='clientTimbrado')],
                [InlineKeyboardButton(
                    'Color de la Carpeta', callback_data='clientColorFolder')],
                [InlineKeyboardButton('Atras', callback_data='main')]]
    # escuchando la eleccion
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
                [InlineKeyboardButton('Main menu', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


# Mensajes de los menus
def mainMenuMessage():
    return 'Opciones:'


def clientConfigMessage():
    return 'Editar Clientes:'


def second_menu_message():
    return 'Choose the submenu in second menu:'

# TODO: hacer que direccione a su duncion correspondiente /cambiarNombre, y espere una respuesta y luego ejecute el cambio


def responseOption(update, context):
    query = update.callback_query
    # CallbackQueries necesita una respuesta para seguir
    query.answer()
    if query.data == 'clientName':
        query.edit_message_text(
            text="Ok. Enviame el nuevo nombre:")


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        allconfig['TOKEN'], use_context=True)

    dp = updater.dispatcher

    # los diferentes comandos para bot
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ayuda', help_command))

    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('export', export_files))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # Handlers del Menu
    updater.dispatcher.add_handler(
        CallbackQueryHandler(mainMenu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(
        clientConfigMenu, pattern='clientConfigMenu'))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_menu, pattern='m2'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientName'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientTimbrado'))
    # updater.dispatcher.add_handler(CallbackQueryHandler(clientConfigSubmenu, pattern='clientColorFolder'))

    updater.dispatcher.add_handler(CallbackQueryHandler(responseOption))

    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_submenu, pattern='m2_1'))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(second_submenu, pattern='m2_2'))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
