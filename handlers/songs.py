import os

from pyrogram import Client
from pyrogram.types import Message, Voice

import youtube_dl
from youtube_search import YoutubeSearch
import requests

from config import BOT_NAME as Bn
from helpers.filters import command, other_filters
from helpers.decorators import errors

@Client.on_message(command("bul") & other_filters)
@errors
async def a(client, message: Message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = await message.reply(f"**{Bn} :-** 🔍 Aranıyor {query}")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## SÜRE SıNıRı ISTIYORSANıZ BUNU KULLANıMDAN KALDıRıLSıN. 1800'LERI KENDI ÖNCEDEN BELIRLENMIŞ SÜRENIZE DEĞIŞTIRIN VE MESAJ (30 dakika üst SıNıRı) SıNıRıNı SANIYELER IÇINDE DÜZENLEYIN
            # if time_to_seconds(duration) >= 1800:  # süre sınırı
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            m.edit(f"**{Bn} :-** 😕 Hiçbir şey bulamadım. Yazımı biraz değiştirmeyi dene..\n\n{e}")
            return
    except Exception as e:
        m.edit(
           f"**{Bn} :-** 😕 Hiçbir şey bulamadım. Üzgünüm.\n\nBaşka bir kelime deneyin veya düzgün düzenleyin."
        )
        print(str(e))
        return
    await m.edit(f"**{Bn} :-** 📥 Indiriyor...\n**Query :-** {query}")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎶 **Başlık:** [{title[:35]}]({link})\n⏳ **Süre:** {duration}\n👀 **Görünümler:** {views}'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await  message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        await m.delete()
    except Exception as e:
        m.edit(f"❌ Hata!! \n\n{e}")
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
