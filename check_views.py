import asyncio
import os
from hydrogram import Client
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
SESSION_STRING = os.getenv('TELEGRAM_SESSION')

async def main():
    if SESSION_STRING:
        app = Client("my_session", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
    else:
        app = Client("my_session", api_id=API_ID, api_hash=API_HASH)
        
    async with app:
        try:
            # fetch one message from the goonies
            async for msg in app.get_chat_history("-1002861009856", limit=1):
                print(f"Message ID: {msg.id}")
                print(f"Views: {msg.views}")
                print(f"Topic: {getattr(msg, 'message_thread_id', None)}")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
