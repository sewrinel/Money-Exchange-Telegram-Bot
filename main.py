from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from .exchange_rate import currencies_dict, currency_rate
from .calculation import purchase_price, cash_price
import jdatetime
import re  # to specify the value/amount that the client types



token: Final = "YOUR_TOKEN"
bot_username: Final = '@YOUR_BOT_ID'
now = jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')



# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام علیکم \nبه ربات metaloex خوش اومدی. ")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات metaloex برای ....")

async def price_inquiry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"قیمت لحظه‌ای در {now} : \nقیمت لحظه‌ای تتر: {currency_rate('تتر')} تومان \nقیمت لحظه‌ای ووچر: {currency_rate('ووچر')} \nدر صورت خرید به اکانت پشتیبانی پی‌ام بدین جناب. \nبرای استعلام قیمت سایر ارزها هم، اسم ارز رو به درستی تایپ کنین"
        )
async def buy_PMUSD_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چقدر میخواین ووچر بخرین جناب؟ لطفا مبلغ رو به تومان بفرستین")
async def cash_PMUSD_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چقدر میخواین ووچر نقد کنین جناب؟ لطفا تعدادش رو بفرستین")

# Responses
def handle_response(text: str) -> str:
    budget_list = re.findall("\d", text)
    if "ووچر" in text:
        return f"جناب! \nقیمت لحظه‌ای ووچر همین الان یعنی {now} : {currency_rate('ووچر')} تومان \nبرای ادامه خرید به اکانت پشتیبانی پی‌ام بدین."
    elif "تتر" in text:
        return f"جناب! \nقیمت لحظه‌ای تتر همین الان یعنی {now} : {currency_rate('تتر')} تومان \nبرای ادامه خرید به اکانت پشتیبانی پی‌ام بدین."
    elif text in currencies_dict.keys():
        return f"قیمت لحظه‌ای {text} در {now} : {currency_rate(text)} تومان"
    elif budget_list:
        num = int("".join(budget_list))
        if num >= 1000000:
            count = purchase_price(currency_rate("ووچر"), num)[0]
            return f"من می‌تونم با این مبلغ {count} ووچر بخرم براتون"
        elif (str(num)[:-4:-1]) == "000": # سه رقم اخر صفر برای تمایز مبلغ خرید و نقد کردن :)  ترتیب ارقام از اخر برعکس میشه
            return "ببخشید جناب ولی من زیر یک تومن ووچر نمی‌گیرم"
        else:
            amount = cash_price(currency_rate("ووچر"), num)
            return f"میتونین {num} ووچر خودتون رو با مبلغ {amount} نقد کنین"
    else:
        return "جناب من رباتم، آدم که نیستم هرچی بگین بفهمم :)))"
    

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(message_type)

    print(f"User ({update.message.chat_id}) in {message_type}: '{text}'")

    # responsing in group/private chat
    if message_type == "group": 
        
        if bot_username in text:
            new_text: str = text.replace(bot_username, "").strip()
            respone: str =  handle_response(new_text)
        else:
            return
    else:
        respone: str = handle_response(text)

    # print("Bot:", respone)
    await update.message.reply_text(respone)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


def main():
    print("starting....")
    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price_inquiry_command))   
    app.add_handler(CommandHandler("cash", cash_PMUSD_command))
    app.add_handler(CommandHandler("buy", buy_PMUSD_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    # app.add_handler(error)

    print("polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
    main()
