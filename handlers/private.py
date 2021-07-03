from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""Ben **{bn}** !!
Grubunuzun sesli sohbetinde müzik çalmanıza izin 😉
Şu anda desteklediğim komutlar şunlardır:
⚜️ /oynat - __Yanıtlanan ses dosyasını veya YouTube videosunu bağlantı üzerinden çalar.__
⚜️ /durdur - __Sesli Sohbet Müziğini Duraklat.__
⚜️ /devam - __Sesli Sohbet Müziğine Devam Et.__
⚜️ /atla - __Sesli Sohbette Çalan Geçerli Müziği Atlar.__
⚜️ /bitir - __Sırayı temizler ve Sesli Sohbet Müziği'ni sona erdirir.__
⚜️ /katil - __Müzik Botunun Asistanını Gruba Çağırır.__
⚜️ /ayril - __Müzik Botunun Asistanını Gruptan Çıkartır.__
⚜️ /bul - __Müziği bulup gruba gönderir. Örnek /bul tuğkan kusura bakma.__
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Grup 💬", url="https://t.me/lunabotnews"
                    ),
                    InlineKeyboardButton(
                        "Kanal 📣", url="https://t.me/lunabotnews"
                    ),
                ]                
                    InlineKeyboardButton(
                        "Kurucu 👨‍💻", url="https://t.me/senseiisttrip"
                    )   
            ]              
        )
    )
