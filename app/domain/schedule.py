from app.domain.api import login, send_sms


async def send_notification(phone_number: str):
    print("[+] Running task")
    token = await login(
        email="valiyevasror10@gmail.com",
        password="bmlvvBs15HCQqP1LH8Ck68tQiQbkq4w71mGIxnjy",
    )
    await send_sms(
        token=token.data.token,
        phone_number=phone_number,
        message="Bu Eskiz dan test",
        from_="Barbershop"
    )
