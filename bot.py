import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telethon import TelegramClient

# लॉगिंग सेट करें
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================
# 🔐 आपकी जानकारी
API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
BOT_TOKEN = '8624071296:AAEfKOdlA_w884R45O0EVGYS7hHM68-HH_g'
CHANNEL = 'ssc_crack_gk'
YOUR_USER_ID = 6362212726
# ========================================

# Telethon Client
telethon_client = TelegramClient('bot_session', API_ID, API_HASH)

async def get_all_polls():
    """चैनल के सभी पोल्स को फॉर्मेट में बदलो"""
    await telethon_client.start()
    all_polls = []
    count = 0
    
    async for msg in telethon_client.iter_messages(CHANNEL, limit=100):
        if msg.poll:
            count += 1
            if hasattr(msg.poll, 'poll'):
                poll = msg.poll.poll
            else:
                poll = msg.poll
            
            answer = "❌ Answer not found (vote on poll first)"
            if hasattr(poll, 'correct_option_id') and poll.correct_option_id is not None:
                c = poll.correct_option_id
                answer = f"✅ Ans: ({chr(65+c)}) {poll.answers[c].text}"
            elif msg.poll.results and hasattr(msg.poll.results, 'results'):
                results = msg.poll.results.results
                for i, res in enumerate(results):
                    if hasattr(res, 'chosen') and res.chosen:
                        answer = f"✅ Ans: ({chr(65+i)}) {poll.answers[i].text}"
                        break
            
            poll_text = f"\n{count}. {poll.question}\n"
            for i, ans in enumerate(poll.answers):
                poll_text += f"({chr(65+i)}) {ans.text}\n"
            poll_text += f"{answer}\n" + "-" * 50
            all_polls.append(poll_text)
    
    return all_polls, count

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 **Quiz Bot Active!**\n\nSend /getpolls to get all quizzes from your channel.")

async def getpolls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Fetching polls from your channel... Please wait.")
    try:
        polls, total = await get_all_polls()
        if polls:
            for poll in polls[:10]:
                await update.message.reply_text(poll)
            await update.message.reply_text(f"✅ **Total polls found: {total}**")
        else:
            await update.message.reply_text("❌ No polls found in your channel.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)[:100]}")

async def run_bot():
    # Bot Application
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getpolls", getpolls))
    
    # Telethon start
    await telethon_client.start()
    logger.info("Telethon client started!")
    
    # Bot start
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    logger.info("Bot is running! Send /getpolls on Telegram.")
    
    # Keep running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(run_bot())
