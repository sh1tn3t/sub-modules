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
import tempfile

from string import hexdigits
from random import choice, randint

from pyrogram import Client, types
from .. import loader, utils


@loader.module(name="TextTools", author="sh1tn3t")
class TextToolsMod(loader.Module):
    """Инструменты для текста"""

    async def switch_cmd(self, app: Client, message: types.Message, args: str):
        """Поменять раскладку текста. Использование: switch <аргументы или реплай>"""
        reply = message.reply_to_message
        text = (
            args
            if args
            else reply.text
            if reply and reply.text
            else reply.caption
            if reply and reply.caption
            else None 
        )
        if not text:
            return await utils.answer(
                message, "<b>[TextTools]</b> Нет аргументов или реплая на текст")

        ru_keys = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё"№;%:?ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"""
        en_keys = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$%^&QWERTYUIOP{}ASDFGHJKL:"|ZXCVBNM<>?"""

        change = str.maketrans(ru_keys + en_keys, en_keys + ru_keys)
        result = str.translate(text, change)

        return await utils.answer(message, result)

    async def mtf_cmd(self, app: Client, message: types.Message, args: str):
        """Текст с реплая в файл. Использование: mtf <реплай на текст> [название]"""
        reply = message.reply_to_message
        if not (reply and reply.text):
            return await utils.answer(
                message, "<b>[TextTools]</b> Нет реплая на текст")

        file_name = (
            "".join(choice(hexdigits) for _ in range(randint(5, 10))) + ".txt"
        ) if not args else args

        file = io.BytesIO(bytes(reply.text, "utf-8"))
        file.name = file_name
        file.seek(0)

        await utils.answer(message, file, doc=True) 
        return await message.delete() 

    async def ftm_cmd(self, app: Client, message: types.Message):
        """Файл в текст. Использование: ftm <реплай на файл>"""
        reply = message.reply_to_message
        if not reply and reply.documemt:
            return await utils.answer(
                message, "<b>[TextTools]</b> Нет реплая на файл")

        file = tempfile.NamedTemporaryFile("w")
        await reply.download(file.name)

        return await utils.answer(
            message, open(file.name, "r").read())
