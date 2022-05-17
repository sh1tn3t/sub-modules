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


@loader.module("BanMedia", "sh1tn3t")
class BanMediaMod(loader.Module):
    """Бан медиа"""

    async def banmedia_cmd(self, app: Client, message: types.Message):
        """Добавить медиа в базу для блокировки. Использование: banmedia <реплай>"""
        chat = message.chat
        if chat.type != "private":
            check_me = await chat.get_member(self.all_modules.me.id)
            if not check_me.can_delete_messages:
                return await utils.answer(
                    message, "<b>[BanMedia - Error]</b> ❌ Нет прав на удаление сообщений")

        reply = message.reply_to_message
        if not reply or not reply.media:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Нет реплая на медиа")

        file_id = utils.get_message_media(reply).file_unique_id
        banned_media = self.db.get("BanMedia", "media", {})

        current_chat = banned_media.setdefault(str(chat.id), [])
        if file_id in current_chat:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Это медиа уже заблокировано")

        current_chat.append(file_id)
        self.db.set("BanMedia", "media", banned_media)
        return await utils.answer(
            message, "<b>[BanMedia]</b> ✅ Медиа добавлено в базу")

    async def unbanmedia_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить медиа из базы для блокировки. Использование: unbanmedia <реплай или all>"""
        reply = message.reply_to_message
        if not reply or not reply.media:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Нет реплая на медиа")

        chat = message.chat

        banned_media = self.db.get("BanMedia", "media", {})
        if not (current_chat := banned_media.setdefault(str(chat.id), [])):
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ В этом чате нет медиа для блокировки")

        file_id = utils.get_message_media(reply).file_unique_id
        if file_id not in current_chat:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Это медиа не заблокировано")

        current_chat.remove(file_id)
        if not current_chat:
            del banned_media[str(chat.id)]

        self.db.set("BanMedia", "media", banned_media)
        return await utils.answer(
            message, "<b>[BanMedia]</b> ✅ Медиа удалено из базы")

    async def banpack_cmd(self, app: Client, message: types.Message):
        """Добавить стикерпак в базу для блокировки. Использование: banpack <реплай на стикер>"""
        chat = message.chat
        if chat.type != "private":
            check_me = await chat.get_member(self.all_modules.me.id)
            if not check_me.can_delete_messages:
                return await utils.answer(
                    message, "<b>[BanMedia - Error]</b> ❌ Нет прав на удаление сообщений")

        reply = message.reply_to_message
        if not reply or not reply.sticker:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Нет реплая на стикер")

        pack_name = reply.sticker.set_name
        banned_packs = self.db.get("BanMedia", "packs", {})

        current_chat = banned_packs.setdefault(str(chat.id), [])
        if pack_name in current_chat:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Этот стикерпак уже заблокирован")

        if not pack_name:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Этот стикер не принадлежит ни к одному паку\n"
                         "🧾 Используй: <code>banmedia</code> <реплай>"
            )

        current_chat.append(pack_name)
        self.db.set("BanMedia", "packs", banned_packs)
        return await utils.answer(
            message, f"<b>[BanMedia]</b> ✅ <a href=\"https://t.me/addstickers/{pack_name}\">Стикерпак</a> добавлен в базу")

    async def unbanpack_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить стикерпак из базы для блокировки. Использование: unbanpack <реплай на стикер или all>"""
        reply = message.reply_to_message
        if not reply or not reply.sticker:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Нет реплая на стикер")

        chat = message.chat
        pack_name = reply.sticker.set_name

        banned_packs = self.db.get("BanMedia", "packs", {})
        if not (current_chat := banned_packs.setdefault(str(chat.id), [])):
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ В этом чате нет стикерпаков для блокировки")

        if pack_name not in current_chat:
            return await utils.answer(
                message, "<b>[BanMedia - Error]</b> ❌ Этот стикерпак не заблокирован")

        current_chat.remove(pack_name)
        if not current_chat:
            del banned_packs[str(chat.id)]

        self.db.set("BanMedia", "packs", banned_packs)
        return await utils.answer(
            message, f"<b>[BanMedia]</b> ✅ <a href=\"https://t.me/addstickers/{pack_name}\">Стикерпак</a> удален из базы")

    async def watcher(self, app: Client, message: types.Message):
        """Отслеживание заблокированных медиа"""
        if not message.media:
            return

        chat = message.chat

        if message.sticker:
            if (
                (pack_name := message.sticker.set_name)
                and (banned_packs := self.db.get("BanMedia", "packs", {}).get(str(chat.id)))
                and pack_name in banned_packs
            ):
                return await message.delete()

        banned_media = self.db.get("BanMedia", "media", {})
        if not (current_chat := banned_media.get(str(chat.id))):
            return

        file_id = utils.get_message_media(message).file_unique_id
        if file_id not in current_chat:
            return

        return await message.delete()
