from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from binance_client import get_historical_data, analyze_signals
from binance.client import Client

# Hàm khởi tạo bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Send Signal", callback_data='send_signal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Press the button below to send the signal.', reply_markup=reply_markup)

# Hàm gửi message khi nhấn nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Giả định bạn đã có hàm get_historical_data và analyze_signals
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_5MINUTE
    limit = 200
    try:
        df = get_historical_data(symbol, interval, limit)
        analysis = analyze_signals(df)

        message = (
            f"\nTime: {analysis['timestamp']}\n"
             f"interval: {interval}\n"
            f"Decision: {analysis['decision']} (Strength: {analysis['strength']:.2f}%)\n"
            f"Current Price: {analysis['current_price']}\n\n"
            "Signal Details:\n"
        )
        for signal in analysis['signals_detail']:
            message += f"- {signal}\n"
        
        message += "\nIndicator Values:\n"
        for indicator, value in analysis['indicators'].items():
            message += f"{indicator}: {value:.2f}\n"
        
        # Gửi message đến nhóm Telegram
        chat_id = query.message.chat_id
        await context.bot.send_message(chat_id=chat_id, text=message)

        await query.edit_message_text(text="Signal sent!")
    except Exception as e:
        await query.edit_message_text(text=f"An error occurred: {e}")

# Hàm chính để chạy bot
def main():
    app = ApplicationBuilder().token("7542004417:AAF43NYwPUG3p9i3CWjXMV6j1C_qIrfZHhM").build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
