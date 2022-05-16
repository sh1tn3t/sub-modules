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

from pyrogram import Client, types, filters
from .. import loader, utils


@loader.module("RPMode", "sh1tn3t")
class RPModeMod(loader.Module):
    """РП режим"""

    async def addrp_cmd(self, app: Client, message: types.Message, args: str):
        """Добавить рп-команду. Использование: addrp <команда> / <сообщение>"""
        if not args:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Не указаны аргументы через \" / \"")

        if args == "/":
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ А ты умный")

        args_ = (" " + args).split(" / ")
        if len(args_) == 1 and args_[0]:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Первый аргумент ты указал, а дальше что?)\n"
                         "🧾 Формат: <code>addrp</code> <команда> / <действие>"
            )

        if len(args_) > 2:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Слишком много аргументов, нужно 2\n"
                         "🧾 Формат: <code>addrp</code> <команда> / <действие>"
            )

        cmd, action = map(
            lambda arg: arg.strip().lower(), args_
        )

        if not cmd:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Не указана команда")

        if not action:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Не указано действие")

        rps = self.db.get("RPMode", "rps", {})
        if cmd in rps:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Такая команда уже есть")

        rps[cmd] = action
        self.db.set("RPMode", "rps", rps)

        return await utils.answer(
            message, f"<b>[RPMode]</b> ✅ Команда \"<code>{cmd}</code>\" добавлена")

    async def delrp_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить рп-команду. Использование: delrp <команда или all_rps_commands>"""
        if not args:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Не указаны аргументы")

        if args == "all_rps_commands":
            self.db.set("RPMode", "rps", {})
            return await utils.answer(
                message, "<b>[RPMode]</b> ✅ Все РП-команды удалены")

        cmd = args.lower()

        rps = self.db.get("RPMode", "rps", {})
        if cmd not in rps:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Такой команды нет")

        del rps[cmd]
        self.db.set("RPMode", "rps", rps)

        return await utils.answer(
            message, f"<b>[RPMode]</b> ✅ Команда \"<code>{args}</code>\" удалена")

    async def rps_cmd(self, app: Client, message: types.Message):
        """Список рп-команд. Использование: rps"""
        rps = self.db.get("RPMode", "rps", {})
        if not rps:
            return await utils.answer(
                message, "<b>[RPMode - Error]</b> ❌ Нет РП-команд")

        text = "<b>[RPMode]</b> 📝 РП-команды:\n\n" + "\n".join(
            f"👉 <code>{cmd}</code> - {rps[cmd]}" for cmd in rps
        )
        return await utils.answer(
            message, text)

    @loader.on(filters.me)
    async def watcher(self, app: Client, message: types.Message):
        """Отслеживание рп-команд"""
        if not (
            (rps := self.db.get("RPMode", "rps", {}))
            and (reply := message.reply_to_message)
            and (m := (message.text or "").lower())
        ):
            return

        ms = m.split(" ")
        matchs = list(filter(lambda rp: rp == ms[0], rps))
        if not matchs:
            return

        match = matchs[-1]
        if len(ms) > 1:
            match += " "

        rp = f"{message.from_user.mention} {rps[matchs[-1]]} {reply.from_user.mention} {m.split(match, 1)[1]}"
        return await utils.answer(
            message, rp)
