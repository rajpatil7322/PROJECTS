from telegram import *
from telegram.ext import * 

BOT_TOKEN = '1932485181:AAGZ1x5X2PloIDYP-9PRjsJIGKIksoO1MOI'
CHANNEL_ID = '-1001545160460'



bot=Bot(BOT_TOKEN)
#print(bot.get_me())
updater=Updater(BOT_TOKEN,use_context=True)

dispatcher=updater.dispatcher

def test_function(update:Updater,context:CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hi i am a bot'
    )


start_value=CommandHandler('motion_detection',test_function)

dispatcher.add_handler(start_value)

updater.start_polling()

    