import base64
import aiohttp
from dotenv import load_dotenv
import os

username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")
api_key = os.getenv("API_KEY")

auth_str = f"{username}:{password}".encode("utf-8")
b64_auth = base64.b64encode(auth_str).decode("ascii")
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/x-www-form-urlencoded"
}

async def get_avr_data():
    url = "http://10.10.70.166/alldata/hs/avr/given"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"apiKey": api_key}, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    except Exception as e:
        print(f"❌ Ошибка при получении данных: {e}")
        return None