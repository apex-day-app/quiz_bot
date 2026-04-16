import asyncio
import os
from telethon import TelegramClient
from telegram import Bot
from telegram.ext import CommandHandler, Application

# ========================================
# 🔐 Environment Variables
API_ID = 35089639
API_HASH = '0c46a9a35e7db749b8a9b87b0bdb0aec'
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Railway से लेगा
CHANNEL = 'ssc_crack_gk'

# Telegram User ID (जहाँ बॉट रिप्लाई भेजेगा)
YOUR_USER_ID = 6362212726

# ========================================

# Telethon Client (तुम्हारे यूजर अकाउंट से)
telethon_client = TelegramClient('bot_session', API_ID, API_HASH)

# Bot
bot = Bot(BOT_TOKEN)

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

async def start_command(update, context):
    await update.message.reply_text("🤖 **Quiz Bot Active!**\n\nSend /getpolls to get all quizzes from your channel.")

async def get_polls_command(update, context):
    await update.message.reply_text("📡 Fetching polls from your channel... Please wait.")
    polls, total = await get_all_polls()
    if polls:
        for poll in polls:
            await update.message.reply_text(poll)
        await update.message.reply_text(f"✅ **Total polls found: {total}**")
    else:
        await update.message.reply_text("❌ No polls found in your channel.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("getpolls", get_polls_command))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
