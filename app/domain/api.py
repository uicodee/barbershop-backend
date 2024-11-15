import aiohttp
from pydantic import TypeAdapter

from app import dto


async def login(email: str, password: str) -> dto.ApiLogin:
    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        # form_data.add_field("email", "valiyevasror10@gmail.com")
        form_data.add_field("email", email)
        # form_data.add_field("password", "bmlvvBs15HCQqP1LH8Ck68tQiQbkq4w71mGIxnjy")
        form_data.add_field("password", password)
        async with session.post(
            url="https://notify.eskiz.uz/api/auth/login", data=form_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                adapter = TypeAdapter(dto.ApiLogin)
                return adapter.validate_python(data)
            else:
                print(await response.text())


async def send_sms(
    token: str, phone_number: str, message: str, from_: str
) -> dto.ApiSend:
    async with aiohttp.ClientSession(
        headers={
            "Authorization": f"Bearer {token}",
        }
    ) as session:
        form_data = aiohttp.FormData()
        form_data.add_field(name="mobile_phone", value=phone_number)
        form_data.add_field(name="message", value=message)
        form_data.add_field(name="from", value=from_)
        async with session.post(
            url="https://notify.eskiz.uz/api/message/sms/send", data=form_data
        ) as response:
            if response.status == 200:
                data = await response.json()
                adapter = TypeAdapter(dto.ApiSend)
                return adapter.validate_python(data)
            else:
                print(await response.text())
