from os import name
from telegram.ext import Updater , CommandHandler , MessageHandler , Filters
import telegram
import json
import pandas as pd
from bot_cred import bot_token , ownerid
import telegram
import requests as rq


bot = telegram.Bot(token=bot_token)
updater = Updater(token = bot_token , use_context=True)




def messg_handler(update , context):
    update.message.reply_text("I'm a certified fool. I only understands /start to give you a free trial🙂")


df = pd.read_csv('cred.csv')
def gen():
    for i in df['creds']:
        yield i

cd = gen()
def start(update , context):
    
    with open('trialusersid.json', "r") as file:
        data = json.load(file)
    try:
        if update.message.chat_id == ownerid:
            update.message.reply_text(f"""Here is the trial credential boss:
            
{next(cd)}""")

        elif update.message.chat_id in data:
            update.message.reply_text("you already used one trial. consider buying a pakage now.")
            

        else:
            entry = update.message.chat_id



            data.append(entry)
    
            with open('trialusersid.json', "w") as file:
                json.dump(data, file)

            update.message.reply_text(f"""Here is the trial credential. paste it there as per tutorial and start using your rocket:
            
{next(cd)}""")
    except StopIteration:
        rs = rq.get(f"https://api.telegram.org/bot1960760901:AAEPNZwRT-YSOtv5hfYyqkcWWLmGsPQcIl0/sendMessage?chat_id={ownerid}&text=[*WARNING] boss trial finished add more.")
        update.message.reply_text("Trial limit finished .I just knocked my owner to add more . you can ask him for one or come back tomorrow:) ")

def downloader(update, context):

    if update.message.chat_id == ownerid:
        with open("cred.csv", 'wb') as f:
            context.bot.get_file(update.message.document).download(out=f)

    else:
        update.message.reply_text("I can't read users files ,too fool 😐 ")

def showall(update,context):
    show = pd.read_csv('cred.csv')
    update.message.reply_text(show)




def help(update, context):
    update.message.reply_text("""normal users:
    /help to get this useless mssg
    /start to get a free trial if eligible
    
    bot owners commands:
    /showall you know what
    upload txt file containing trial cred *must give first line \"creds\" word and from next lines 1 line = 1 trial cred""")
    


botcmds = [
    ('/start', 'get a trial'),
    ('/help',  'get useless help')
    ]

bot.set_my_commands(botcmds)



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('showall', showall))
updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader))
updater.dispatcher.add_handler(MessageHandler(telegram.ext.Filters.text , messg_handler))

updater.start_polling()
updater.idle
