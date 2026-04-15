from telethon import TelegramClient
import asyncio

# 🔐 आपकी API जानकारी
api_id = 35089639
api_hash = '0c46a9a35e7db749b8a9b87b0bdb0aec'

# 📢 आपका चैनल (बिना @ के)
CHANNEL = 'ssc_crack_gk'

# आपका Telegram User ID
YOUR_USER_ID = 6362212726

client = TelegramClient('bot_session', api_id, api_hash)

async def get_all_polls():
    """चैनल के सभी पोल्स को फॉर्मेट में बदलो"""
    all_polls = []
    count = 0
    
    async for msg in client.iter_messages(CHANNEL, limit=100):
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

async def send_to_me(message):
    await client.send_message(YOUR_USER_ID, message)

async def main():
    await client.start()
    print("✅ Login successful!")
    await send_to_me("🤖 Bot Active! Send /getpolls")
    
    @client.on(events.NewMessage)
    async def handle_message(event):
        if event.sender_id == YOUR_USER_ID and event.message.text == '/getpolls':
            await send_to_me("📡 Fetching polls...")
            polls, total = await get_all_polls()
            for p in polls:
                await send_to_me(p)
            await send_to_me(f"✅ Total polls: {total}")
    
    await client.run_until_disconnected()

asyncio.run(main())
