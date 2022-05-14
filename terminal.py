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

import asyncio

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Terminal", "sh1tn3t")
class TerminalMod(loader.Module):
    """Бюджетный терминал"""

    async def terminal_cmd(self, app: Client, message: types.Message, args: str):
        """Выполняет команду в терминале. Использование: terminal <команда>"""
        proc = await asyncio.create_subprocess_shell(
            args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()
        text = (
            f"<b>Команда:</b> <code>{args}</code>\n"
            f"<b>Код возврата:</b> <code>{proc.returncode}</code>\n"
            f"<b>Вывод:</b>\n<code>{stdout.decode()}</code>\n\n"
            f"<b>Ошибки:</b>\n<code>{stderr.decode()}</code>"
        )

        return await utils.answer(
            message, text)
