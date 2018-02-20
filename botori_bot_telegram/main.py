import telegram
import datetime
import threading
from Crawler import MainCrawler

INTERVAL_BOT_SEC = 20
INTERVAL_UPDATE_CHECK = 2

my_token = '498746306:AAEBTsIQVHqrNhcwpHji1yCfycUsx4Brg5Y'
bot = telegram.Bot(token = my_token)
ownerChatId = ""
crawler = MainCrawler()
flag_bus_bot = True
doBotAction = False
prev_flag_bus_bot = flag_bus_bot
msgId = 0

def telegramBotUpdate():
    global ownerChatId
    global flag_bus_bot
    global INTERVAL_BOT_SEC
    global doBotAction
    global msgId

    try:
        updates = bot.getUpdates()
        for u in updates : 
            if (ownerChatId == ""):
                ownerChatId = u.message.chat.id

        if (len(updates) > 0):
            lastMsg = updates[len(updates) - 1].message
            txt = lastMsg.text
            
            if lastMsg.message_id == msgId:
               return

            if "/stop_bus" in txt:
                flag_bus_bot = False
                pass
            elif "/start_bus" in txt:
                flag_bus_bot = True
                params = txt.split('=')
                if len(params) > 1:
                    INTERVAL_BOT_SEC = max(3, int(params[1]))
                pass
            elif "/rp" in txt:
                runRipplePriceBot()
                pass

            msgId = lastMsg.message_id
    finally:
        threading.Timer(INTERVAL_UPDATE_CHECK, telegramBotUpdate).start()
    pass

def runBusBot():
    try:
        global prev_flag_bus_bot

        cTime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')

        if prev_flag_bus_bot != flag_bus_bot:
            sendMessageToMaster("/start_bus" if flag_bus_bot else "/stop_bus")

        prev_flag_bus_bot = flag_bus_bot        

        if flag_bus_bot == False or ownerChatId == "":
            threading.Timer(INTERVAL_UPDATE_CHECK, runBusBot).start()
            return

        res = crawler.run_companyToHome()
        
        botMsg = '''
회사 -> 집 (정류장:23202)
-----------------------
{0}
(1): {1}
(2): {2}
        '''.format(cTime, res['res1'], res['res2'])

        sendMessageToMaster(botMsg)
        threading.Timer(INTERVAL_BOT_SEC, runBusBot).start()
    except:
        threading.Timer(INTERVAL_BOT_SEC, runBusBot).start()
    pass

def runRipplePriceBot():
    price = crawler.run_rippleRealtimePrice()
    msg = '''
리플 현재가격
--------------------
{0}
    '''.format(price)
    sendMessageToMaster(msg)
    pass

def sendMessageToMaster(msg):
    if ownerChatId == "":
        return
    bot.sendMessage(chat_id = ownerChatId, text = msg)
    pass


if __name__ == '__main__':
    telegramBotUpdate()
    runBusBot()
    print('run - botori_bot_telegram')
    pass

