from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from binance_client import get_historical_data, analyze_signals
from binance.client import Client
from common import generate_content

# Hàm khởi tạo bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Add button to send the signal message
    keyboard = [[InlineKeyboardButton("Send Signal", callback_data='send_signal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Press the button below to send the signal.', reply_markup=reply_markup)

# Hàm gửi message khi nhấn nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Set parameters for analysis
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_5MINUTE
    limit = 200
    try:
        # Get historical data and perform analysis
        df = get_historical_data(symbol, interval, limit)
        analysis = analyze_signals(df)

        # Format message
        message = (
            f"\nTime: {analysis['timestamp']}\n"
            f"Interval: {interval}\n"
            f"Decision: {analysis['decision']} (Strength: {analysis['strength']:.2f}%)\n"
            f"Current Price: {analysis['current_price']}\n\n"
            "Signal Details:\n"
        )
        for signal in analysis['signals_detail']:
            message += f"- {signal}\n"
        
        message += "\nIndicator Values:\n"
        for indicator, value in analysis['indicators'].items():
            message += f"{indicator}: {value:.2f}\n"

        # Send formatted message to the chat
        chat_id = query.message.chat_id
        await context.bot.send_message(
            chat_id=chat_id,
            text=generate_content("ĐÂY LÀ DỮ LIỆU CỤ THỂ Ở THỜI ĐIỂM HIỆN TAI HÃY PHÂN TÍCH 1 CÁCH CỤ THỂ CHI TIẾT ĐỂ TÔI HIỂU ĐƯỢC" + message)
        )

        # Confirm message sent
        await query.edit_message_text(text="Signal sent!")
    except Exception as e:
        # Handle errors by notifying user
        await query.edit_message_text(text=f"An error occurred: {e}")

# Hàm ghi lại tin nhắn người dùng gửi đến bot
async def log_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     # Capture the user's message
    user_message = update.message.text

    # Send a response back to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=generate_content(user_message)
    )

# Hàm chính để chạy bot
def main():
    # Initialize bot application
    app = ApplicationBuilder().token("7542004417:AAF43NYwPUG3p9i3CWjXMV6j1C_qIrfZHhM").build()

    # Register command and callback handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    # Register message handler to log incoming messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log_message))

    # Run the bot
    app.run_polling()

if __name__ == '__main__':
    main()
