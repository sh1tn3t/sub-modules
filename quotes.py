#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import io
import json
import base64

import requests
import tempfile

from time import gmtime
from typing import List, Union

from pyrogram import Client, types
from pyrogram.errors import RPCError

from .. import loader, utils


def get_message_media(message: types.Message):
    return message.photo or message.sticker or message.video or message.video_note or message.animation or message.web_page


def strftime(time: Union[int, float]):
    t = gmtime(time)
    return (
        f"{t.tm_hour:02d}:"
        if t.tm_hour > 0
        else ""
    ) + f"{t.tm_min:02d}:{t.tm_sec:02d}"


def get_message_text(message: types.Message, reply: bool = False):
    return (
        "📷 Фото"
        if message.photo and reply
        else message.sticker.emoji or "" + " Стикер"
        if message.sticker and reply
        else "📹 Видеосообщение"
        if message.video_note and reply
        else "📹 Видео"
        if message.video and reply
        else "🖼 GIF"
        if message.animation and reply
        else "📊 Опрос"
        if message.poll
        else "📍 Местоположение"
        if message.location
        else "👤 Контакт"
        if message.contact
        else "🎮 Игра"
        if message.game
        else f"🎵 Голосовое сообщение: {strftime(message.voice.duration)}"
        if message.voice
        else f"🎧 Музыка: {strftime(message.audio.duration)} | {message.audio.performer} - {message.audio.title}"
        if message.audio
        else f"💾 Файл: {message.document.file_name}"
        if message.document and not get_message_media(message)
        else f"{message.dice.emoji} Дайс: {message.dice.value}"
        if message.dice
        else "Service message"
        if message.service
        else ""
    )


@loader.module(name="Quotes", author="sh1tn3t")
class QuotesMod(loader.Module):
    """Квоты от @sh1tn3t'а"""

    strings = {
        "no_reply": "<b>[Quotes]</b> Нет реплая",
        "processing": "<b>[Quotes]</b> Обработка...",
        "api_processing": "<b>[Quotes]</b> Ожидание API...",
        "api_error": "<b>[Quotes]</b> Ошибка API",
        "loading_media": "<b>[Quotes]</b> Отправка...",
        "no_args_or_reply": "<b>[Quotes]</b> Нет аргументов или реплая",
        "args_error": "<b>[Quotes]</b> При обработке аргументов произошла ошибка. Запрос был: <code>{}</code>",
        "too_many_messages": "<b>[Quotes]</b> Слишком много сообщений. Максимум: <code>{}</code>"
    }

    def __init__(self):
        self.api_endpoint = "https://quotes.fl1yd.su/generate"
        self.settings = self.get_settings()

    async def q_cmd(self, app: Client, message: types.Message, args: str):
        """Сокращение команды quote"""
        return await self.quote_cmd(app, message, args)

    async def quote_cmd(self, app: Client, message: types.Message, args: str):
        """Использование:

        • quote <кол-во сообщений> + <реплай> + [!file - скидывает файлом] + [цвет]
        >>> quote
        >>> quote 2 #2d2d2d
        >>> quote red
        >>> quote !file"""

        args = args.split()
        reply = message.reply_to_message
        if not reply:
            return await utils.answer(
                message, self.strings["no_reply"])

        isFile = "!file" in args
        [count] = list(
            map(int, filter(
                lambda arg: arg.isdigit() and int(arg) > 0, args)
            )
        ) or [1]
        [color] = list(
            filter(
                lambda arg: arg != "!file" and not arg.isdigit(), args)
        ) or ["#152331"]

        if count > self.settings["max_messages"]:
            return await utils.answer(
                message, self.strings["too_many_messages"])

        m = await utils.answer(
            message, self.strings["processing"].format(
                self.settings["max_messages"])
        )

        payload = {
            "messages": await self.quote_parse_messages(app, message, count),
            "quote_color": color,
            "text_color": self.settings["text_color"]
        }

        if self.settings["debug"]:
            file = open("QuotesDebug.json", "w")
            json.dump(
                payload, file, indent=4,
                ensure_ascii=False,
            )
            await utils.answer(
                m, file.name, doc=True)

        await utils.answer(
            m, self.strings["api_processing"])

        r = await self._api_request(payload)
        if r.status_code != 200:
            return await utils.answer(
                m, self.strings["api_error"])

        await utils.answer(
            m, self.strings["loading_media"])

        quote = io.BytesIO(r.content)
        quote.name = "Quote" + (
            ".png" if isFile else ".webp")

        await utils.answer(message, quote, doc=True)
        return await m[-1].delete()


    async def quote_parse_messages(self, app: Client, message: types.Message, count: int):
        payloads: List[dict] = []
        messages: List[types.Message] = [
            msg async for msg in app.iter_history(
                message.chat.id, count, reverse=True,
                offset_id=message.reply_to_message.message_id
            )
        ]

        for message in messages:
            avatar = rank = reply_id = reply_name = reply_text = None

            entities = message.entities or message.caption_entities or []
            entities = list(
                map(
                    json.loads, map(str, entities)
                )
            )

            if forwarded := await self.get_forwarded_message(app, message):
                user_id, name, avatar = forwarded
            else:
                user = message.from_user
                user_id = user.id
                name, avatar = await self.get_profile_data(app, user)

                reply = message.reply_to_message
                if reply and not reply.empty:
                    if forwarded := await self.get_forwarded_message(app, reply):
                        reply_id, reply_name, _ = forwarded
                    else:
                        reply_id = reply.from_user.id
                        reply_name = utils.get_display_name(reply.from_user)

                    reply_text = get_message_text(reply, True) + (
                        ". " + reply.text
                        if reply.text and get_message_text(reply, True)
                        else reply.text or ""
                    )

                if message.chat.type != "private":
                    check_user = await message.chat.get_member(user_id)
                    rank = check_user.title or (
                        "admin" if check_user.status == "administrator"
                        else "creator" if check_user.status == "creator"
                        else ""
                    )

            via_bot = message.via_bot.username if message.via_bot else None
            if media := get_message_media(message):
                with tempfile.NamedTemporaryFile("wb", delete=True) as file:
                    media = await app.download_media(media.thumbs[-1].file_id if media.thumbs else media.file_id, file.name)
                    media = base64.b64encode(open(file.name, "rb").read()).decode()

            text = message.text or message.caption
            text = (
                (text or "") + (
                    (
                        "\n\n" + get_message_text(message)
                        if text
                        else get_message_text(message)
                    )
                    if get_message_text(message)
                    else ""
                )
            )

            payloads.append(
                {
                    "text": text,
                    "media": media,
                    "entities": entities,
                    "author": {
                        "id": user_id,
                        "name": name,
                        "avatar": avatar,
                        "rank": rank or "",
                        "via_bot": via_bot
                    },
                    "reply": {
                        "id": reply_id,
                        "name": reply_name,
                        "text": reply_text
                    }
                }
            )

        return payloads


    async def fq_cmd(self, app: Client, message: types.Message, args: str):
        """Использование:

        • fq <@ или ID> + <текст> - квота от юзера с @ или ID + указанный текст
        >>> fq @onetimeusername Вам пизда

        • fq <реплай> + <текст> - квота от юзера с реплая + указанный текст
        >>> fq Я лох

        • fq <@ или ID> + <текст> + -r + <@ или ID> + <текст> - квота с фейковым реплаем
        >>> fq @Fl1yd спасибо -r @onetimeusername Ты крутой

        • fq <@ или ID> + <текст> + -r + <@ или ID> + <текст>; <аргументы> - квота с фейковыми мульти сообщениями
        >>> fq @onetimeusername Пацаны из @sh1tchannel, ждите награду за ахуенный ботнет; @spypm чево; @Fl1yd НАШ БОТНЕТ ЛУЧШИЙ -r @spypm чево"""

        reply = message.reply_to_message
        if not (args or reply):
            return await utils.answer(
                message, self.strings["no_args_or_reply"])

        m = await utils.answer(
            message, self.strings["processing"])

        try:
            payload = await self.fakequote_parse_messages(app, args, reply)
        except (IndexError, ValueError):
            return await utils.answer(
                m, self.strings["args_error"].format(
                    message.text)
            )

        if len(payload) > self.settings["max_messages"]:
            return await utils.answer(
                m, self.strings["too_many_messages"].format(
                    self.settings["max_messages"])
            )

        payload = {
            "messages": payload,
            "quote_color": self.settings["bg_color"],
            "text_color": self.settings["text_color"]
        }

        if self.settings["debug"]:
            file = open("QuotesDebug.json", "w")
            json.dump(
                payload, file, indent=4,
                ensure_ascii=False,
            )
            await utils.answer(
                m, file.name, doc=True)

        await utils.answer(
            m, self.strings["api_processing"])

        r = await self._api_request(payload)
        if r.status_code != 200:
            return await utils.answer(
                m, self.strings["api_error"])

        quote = io.BytesIO(r.content)
        quote.name = "Quote.webp"

        await utils.answer(m, quote, doc=True)
        return await m[-1].delete()


    async def fakequote_parse_messages(self, app: Client, args: str, reply: types.Message):
        async def get_user(args: str):
            args_ = args.split()
            text = ""

            user = await app.get_chat(
                int(args_[0]) if args_[0].isdigit()
                else args_[0]
            )
            if len(args_) < 2:
                user = await app.get_chat(
                    int(args) if args.isdigit()
                    else args
                )
            else:
                text = args.split(maxsplit=1)[1]
            return user, text

        if reply or reply and args:
            text = args or ""
            user = reply.from_user
            name, avatar = await self.get_profile_data(app, user)

        else:
            messages = []
            for part in args.split("; "):
                user, text = await get_user(part)
                name, avatar = await self.get_profile_data(app, user)
                reply_id = reply_name = reply_text = None

                if " -r " in part:
                    user, text = await get_user(''.join(part.split(" -r ")[0]))
                    user2, text2 = await get_user(''.join(part.split(" -r ")[1]))

                    name, avatar = await self.get_profile_data(app, user)
                    name2, _ = await self.get_profile_data(app, user2)

                    reply_id = user2.id
                    reply_name = name2
                    reply_text = text2

                messages.append(
                    {
                        "text": text,
                        "media": None,
                        "entities": None,
                        "author": {
                            "id": user.id,
                            "name": name,
                            "avatar": avatar,
                            "rank": ""
                        },
                        "reply": {
                            "id": reply_id,
                            "name": reply_name,
                            "text": reply_text
                        }
                    }
                )
            return messages

        return [
            {
                "text": text,
                "media": None,
                "entities": None,
                "author": {
                    "id": user.id,
                    "name": name,
                    "avatar": avatar,
                    "rank": ""
                },
                "reply": {
                    "id": None,
                    "name": None,
                    "text": None
                }
            }
        ]


    async def sqset_cmd(self, app: Client, message: types.Message, args: str):
        """Использование:

        • sqset <bg_color/text_color/debug> (<цвет для bg_color/text_color> <True/False для debug>)
        >>> sqset bg_color #2d2d2d
        >>> sqset debug true"""

        args: args.split(maxsplit=1)
        if not args:
            return await utils.answer(
                message,
                f"<b>[Quotes]</b> Настройки:\n\n"
                f"Максимум сообщений (<code>max_messages</code>): {self.settings['max_messages']}\n"
                f"Цвет квоты (<code>bg_color</code>): {self.settings['bg_color']}\n"
                f"Цвет текста (<code>text_color</code>): {self.settings['text_color']}\n"
                f"Дебаг (<code>debug</code>): {self.settings['debug']}\n\n"
                f"Настроить можно с помощью <code>.sqset</code> <параметр> <значение> или <code>reset</code>"
            )

        if args[0] == "reset":
            self.get_settings(True)
            return await utils.answer(
                message, "<b>[Quotes - Settings]</b> Настойки квот были сброшены")

        if len(args) < 2:
            return await utils.answer(
                message, "<b>[Quotes - Settings]</b> Недостаточно аргументов")

        mods = ["max_messages", "bg_color", "text_color", "debug"]
        if args[0] not in mods:
            return await utils.answer(
                message, f"<b>[Quotes - Settings]</b> Такого парамерта нет, есть {', '.join(mods)}")

        elif args[0] == "debug":
            if args[1].lower() not in ["true", "false"]:
                return await utils.answer(
                    message, "<b>[Quotes - Settings]</b> Такого значения параметра нет, есть true/false")
            self.settings[args[0]] = args[1].lower() == "true"

        elif args[0] == "max_messages":
            if not args[1].isdigit():
                return await utils.answer(
                    message, "<b>[Quotes - Settings]</b> Это не число")
            self.settings[args[0]] = int(args[1])

        else:
            self.settings[args[0]] = args[1]

        self.db.set("Quotes", "settings", self.settings)
        return await utils.answer(
            message, f"<b>[Quotes - Settings]</b> Значение параметра {args[0]} было выставлено на {args[1]}")


    async def get_profile_data(self, app: Client, user: types.User, only_avatar: bool = False):
        avatar = None
        if avatars := await app.get_profile_photos(user.id if not only_avatar else user, limit=1):
            with tempfile.NamedTemporaryFile("wb", delete=True) as file:
                avatar = await app.download_media(avatars[0].file_id, file.name)
                avatar = base64.b64encode(open(file.name, "rb").read()).decode()
        if only_avatar:
            return avatar

        return utils.get_display_name(user), avatar


    async def get_forwarded_message(self, app: Client, message: types.Message):
        avatar = None
        if message.forward_from:
            user_id = message.forward_from.id                    
            name = utils.get_display_name(message.forward_from)

        elif name := message.forward_sender_name:
            user_id = message.chat.id

        elif message.forward_from_chat:
            user_id = message.forward_from_chat.id
            name = message.forward_from_chat.title
            try:
                avatar = await self.get_profile_data(
                    app, user_id if user_id != message.chat.id else None, True)
            except RPCError:
                pass
        else:
            return None

        return user_id, name, avatar


    def get_settings(self, force: bool = False):
        settings: dict = self.db.get(
            "Quotes", "settings", {}
        )
        if not settings or force:
            settings.update(
                {
                    "max_messages": 15,
                    "bg_color": "#162330",
                    "text_color": "#fff",
                    "debug": False
                }
            )
            self.db.set("Quotes", "settings", settings)

        return settings


    async def _api_request(self, data: dict):
        return await utils.run_sync(
            requests.post, self.api_endpoint, json=data
        )