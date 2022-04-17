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

import os
import re

import io
import requests

from random import randint, choice
from string import hexdigits

from pyrogram import Client, types

from .. import loader, utils


@loader.module("Downloader", "sh1tn3t")
class DownloaderMod(loader.Module):
    """Скачивает что угодно"""

    async def dlr_cmd(self, app: Client, message: types.Message, args: str):
        """Скачивает медиа или текст с реплая. Использование: dlr <реплай> [название]"""
        reply = message.reply_to_message
        if not reply:
            return await utils.answer(
                message, "Нет реплая")

        if reply.media:
            file_path = await reply.download(args)
        else:
            file_name = (
                "".join(choice(hexdigits) for _ in range(randint(5, 10))) + ".txt"
            ) if not args else args
            file = open(f"{file_name}", "w")
            file.write(reply.text or reply.caption)

            file_path = file.name

        return await utils.answer(
            message, f"Файл <code>{file_path.split('/')[-1]}</code> был загружен\n\n"
                     f"Выгрузить его можно с помощь команды <code>ulf {file_path}</code>"
        )

    async def ulf_cmd(self, app: Client, message: types.Message, args: str):
        """Выгрузить файл (по ссылке тоже). Использование: ulf <название или путь до файла>"""
        reply = message.reply_to_message
        if not (args or reply):
            return await utils.answer(
                message, "Нет аргументов или реплая")

        regex = re.compile(
            r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|"
            r"www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|"
            r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|"
            r"www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        )
        if (match := regex.search(args or reply.text)):
            args = match.group(0)

            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                return await utils.answer(
                    message, "Не удалось запрос к сайту")

            file = io.BytesIO(r.content)
            file.name = args.split("/")[-1]
            file.seek(0)

            msg = await utils.answer(
                message, f"Отправка файла по ссылке <code>{args}</code>...")

        elif args:
            if not os.path.exists(args):
                return await utils.answer(
                    message, f"Такого файла не существует\n"
                            f"Запрос был <code>{args}</code>"
                )

            file = args
            msg = await utils.answer(
                message, "Отправка...")
        else:
            return await utils.answer(
                message, "В реплае нет ссылки")

        await utils.answer(message, file, quote=False, doc=True)
        return await msg[-1].delete()
