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


@loader.module("Triggers", "sh1tn3t")
class TriggersMod(loader.Module):
    """Триггеры на сообщения"""

    async def trigger_cmd(self, app: Client, message: types.Message, args: str):
        """Добавить триггер. Использование: trigger <аргумент (триггер)> <реплай (ответ на триггер)> или trigger <аргумент // реплай>"""
        reply = message.reply_to_message
        if not reply:
            if not args:
                return await utils.answer(
                    message, "Нет аргументов и реплая")

            if " // " not in args:
                return await utils.answer(
                    message, "В аргументах нет \"<code> // </code>\" разделяющего триггер и ответа")

            key, value = args.split(" // ", 1)
        else:
            if not args:
                return await utils.answer(
                    message, "Нет аргументов")

            key, value = args, reply

        triggers = self.db.get("Triggers", "chats", {})
        chat_triggers = triggers.setdefault(str(message.chat.id), {})

        if key in chat_triggers:
            return await utils.answer(
                message, "Такой триггер уже есть")

        msg = await self.db.save_data(value)
        chat_triggers[key] = msg.message_id

        self.db.set("Triggers", "chats", triggers)
        return await utils.answer(
            message, f"Триггер \"<code>{key}</code>\" сохранён")

    async def stop_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить триггер. Использование: stop <аргумент (триггер)>"""
        chat_id = str(message.chat.id)

        if not args:
            return await utils.answer(
                message, "Нет аргументов")

        triggers = self.db.get("Triggers", "chats", {})
        chat_triggers = triggers.get(chat_id, {})

        if not chat_triggers:
            return await utils.answer(
                message, "Триггеры в этом чате отсутствуют")

        if args == "all":
            del triggers[chat_id]
            self.db.set("Triggers", "chats", triggers)
            return await utils.answer(
                message, "Все триггеры в этом чате удалены")

        if args not in chat_triggers:
            return await utils.answer(
                message, "Такого триггера нет")

        del chat_triggers[args]
        if not chat_triggers:
            del triggers[chat_id]

        self.db.set("Triggers", "chats", triggers)
        return await utils.answer(
            message, f"Триггер \"{args}\" удалён")

    async def triggers_cmd(self, app: Client, message: types.Message):
        """Показать список триггеров. Использование: triggers"""
        triggers = self.db.get("Triggers", "chats", {})
        chat_triggers = triggers.get(str(message.chat.id), {})

        if not chat_triggers:
            return await utils.answer(
                message, "Триггеры отсутствуют")

        text = "\n".join(
            map("• <code>{}</code>".format, chat_triggers.keys())
        )
        return await utils.answer(
            message, f"Список триггеров:\n\n{text}")

    async def watcher(self, app: Client, message: types.Message):
        """Отслеживание триггеров"""
        triggers = self.db.get("Triggers", "chats", {})
        chat_triggers = triggers.get(str(message.chat.id), {})
        if not chat_triggers:
            return

        if not (text := (message.text or message.caption)):
            return

        for part in text.split():
            if part in chat_triggers:
                msg: types.Message = await self.db.get_data(chat_triggers[part])
                await msg.copy(
                    message.chat.id,
                    reply_to_message_id=message.message_id
                )
