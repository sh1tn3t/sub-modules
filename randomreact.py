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

import logging
import random

from pyrogram import Client, types, filters, errors
from .. import loader, utils


@loader.module("RandomReact", "sh1tn3t")
class RandomReactMod(loader.Module):
    """Ставит реакции рандомные реакции"""

    async def react_cmd(self, app: Client, message: types.Message, args: str):
        """Включить/выключить рандомные реакции. Использование: react [шанс (в %, от 1 до 100)]"""
        chat = message.chat
        if chat.type not in ["group", "supergroup"]:
            return await utils.answer(
                message, "❌ <b>Это не чат</b>")

        chats = self.db.get("RandomReact", "chats", {})
        if args or not chats.get(str(chat.id)):
            chance = (
                int(args) if args.isdigit() and 0 < int(args) <= 100
                else 30
            )
            chats[str(chat.id)] = {
                "on": True,
                "chance": chance,
                "reactions": (await app.get_chat(chat.id)).available_reactions
            }

            self.db.set("RandomReact", "chats", chats)
            return await utils.answer(
                message, f"👍🏿 <b>Автоматическое выставление реакций включено!</b>\n"
                         f"Шанс срабатывания: <b>{chance}</b>%"
            )

        del chats[str(chat.id)]
        self.db.set("RandomReact", "chats", chats)
        return await utils.answer(
            message, "👎 <b>Автоматическое выставление реакций отключено</b>")

    @loader.on(~filters.outgoing & filters.group)
    async def watcher(self, app: Client, message: types.Message):
        """Ставит реакции"""
        chat = message.chat

        chats = self.db.get("RandomReact", "chats", {})
        if not (current_chat := chats.get(str(chat.id))):
            return

        chance = current_chat["chance"]
        if random.randint(0, 100) >= chance:
            return

        reactions = current_chat["reactions"]
        if not reactions:
            return

        try:
            await app.send_reaction(
                chat.id, message.message_id,
                random.choice(reactions)
            )
        except errors.RPCError as error:
            logging.exception(error)
