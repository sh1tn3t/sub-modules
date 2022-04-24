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

from pyrogram import Client, types
from .. import loader, utils


@loader.module("Notes", "sh1tn3t")
class NotesMod(loader.Module):
    """Заметки"""

    async def note_cmd(self, app: Client, message: types.Message, args: str):
        """Вызвать заметку. Использование: note <название>"""
        reply = message.reply_to_message
        if not args:
            return await utils.answer(
                message, "Нет аргументов")

        notes = self.db.get("sh1t-ub.modules", "notes", {})
        if args not in notes:
            return await utils.answer(
                message, "Такой заметки нет")

        msg = await self.db.get_data(notes[args])
        await msg.copy(
            message.chat.id, reply_to_message_id=(
                reply.message_id if reply else None)
        )

        return await message.delete()

    async def save_cmd(self, app: Client, message: types.Message, args: str):
        """Сохранить заметку. Использование: save <реплай> <название>"""
        reply = message.reply_to_message
        if not (args and reply):
            return await utils.answer(
                message, "Нет аргументов и реплая")

        notes = self.db.get("sh1t-ub.modules", "notes", {})

        if reply:
            if not args:
                return await utils.answer(
                    message, "Нет аргументов")
            else:
                if args in notes:
                    return await utils.answer(
                        message, "Заметка с таким названием уже есть")
        else:
            return await utils.answer(
                message, "Нет реплая")

        msg = await self.db.save_data(reply)
        notes.setdefault(args, msg.message_id)

        self.db.set("sh1t-ub.modules", "notes", notes)
        return await utils.answer(
            message, f"Заметка \"<code>{args}</code>\" сохранена!")

    async def delnote_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить заметку. Использование: delnote <название>"""
        notes = self.db.get("sh1t-ub.modules", "notes", {})

        if not args:
            return await utils.answer(
                message, "Нет аргументов")

        if args not in notes:
            return await utils.answer(
                message, "Такой заметки нет")

        notes.pop(args)

        self.db.set("sh1t-ub.modules", "notes", notes)
        return await utils.answer(
            message, f"Заметка \"<code>{args}</code>\" удалена!")

    async def notes_cmd(self, app: Client, message: types.Message):
        """Вывести список всех заметок. Использование: notes"""
        notes = self.db.get("sh1t-ub.modules", "notes", {})
        if not notes:
            return await utils.answer(
                message, "Список заметок нет")

        text = "\n".join(map("• <code>{}</code>".format, notes))
        return await utils.answer(
            message, f"Список заметок:\n{text}")

    async def findnote_cmd(self, app: Client, message: types.Message, args: str):
        """Найти ссылку на заметку по названию. Использование: findnote <название>"""
        notes = self.db.get("sh1t-ub.modules", "notes", {})

        if not args:
            return await utils.answer(
                message, "Нет аргументов")

        if args not in notes:
            return await utils.answer(
                message, "Такой заметки нет")

        msg = await self.db.get_data(notes[args])
        return await utils.answer(
            message, f"Ссылка на заметку \"<code>{args}</code>\":\n"
                     f"{msg.link}"
        )
