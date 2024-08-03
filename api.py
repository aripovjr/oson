import aiohttp
from config import URL


async def check_user_by_id(telegram_id: int):
    async with aiohttp.ClientSession() as session:
        url = URL + "/accounts/check_id/?telegram_id={}".format(telegram_id)
        async with session.get(url, ssl=False) as response:
            if response.status not in [200, 201]:
                return False
            return await response.json()


async def check_user_by_phone(user_phone: str):
    async with aiohttp.ClientSession() as session:
        print(user_phone)
        if not user_phone.startswith("+"):
            user_phone = f"+{user_phone}"
        print(user_phone)
        url = URL + f'/accounts/check_number/?phone_number={user_phone}/'
        payload={
            "phone_number": user_phone
        }
        async with session.get(url, data=payload, ssl=False) as response:
            print(21, await response.json())
            if response.status not in [200, 201]:
                return False
            return await response.json()


async def reset_password(password: str, user_id: int, telegram_id: int):
    url = URL + f"/accounts/update_profile_for_bot/{user_id}/"
    payload = {"user": {"telegram_id": telegram_id,"password": password}}
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, ssl=False) as response:
            result = await response.json()
            print(37, result.get("user"))
            if response.status not in [200, 201]:
                return {"error": result.get("detail", "Unknown error")}
            return result
