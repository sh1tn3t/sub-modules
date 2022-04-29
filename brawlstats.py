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

from brawlstats import Client as BrawlStatsClient
from brawlstats.errors import Forbidden, NotFoundError
from brawlstats.models import Club, Player

from pyrogram import Client, types
from .. import loader, utils


@loader.module("BrawlStats", "sh1tn3t")
class BrawlStatsMod(loader.Module):
    """Статистика BrawlStars"""

    async def bs_token_cmd(self, app: Client, message: types.Message, args: str):
        """Токен брать на developer.brawlstars.com. Использование: bs_token <токен>"""
        if not args:
            return await utils.answer(
                message, "Не указан токен. Возьми его на developer.brawlstars.com")

        self.db.set("BrawlStats", "token", args)
        return await utils.answer(
            message, "<b>[BrawlStats]</b> Токен установлен")

    async def bsprofile_cmd(self, app: Client, message: types.Message, args: str):
        """Получить информацию о игроке. Использование: bsprofile <тег> [любой аргумент - выведет только всех бойцов игрока]"""
        try:
            client = BrawlStatsClient(self.db.get("BrawlStats", "token", "дурак токен укажи"), is_async=True)
        except Forbidden:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Токен не указан или указан неверно")

        args = args.upper().split()
        if not args:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Не указан тег игрока")

        try:
            player: Player = await client.get_player(args[0])
        except NotFoundError:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Не удалось найти игрока")

        text = (
            f"<b>Ник:</b> {player.name} (<code>{player.tag}</code>)\n"
            f"<b>Уровень:</b> {player.exp_level}\n"
            f"<b>Трофеи:</b> {player.trophies} (макс.: {player.highest_trophies})\n\n"
            f"<b>Соло победы:</b> {player.solo_victories}\n"
            f"<b>Дуо победы:</b> {player.duo_victories}\n"
            f"<b>Трио победы:</b> {player.team_victories}" + (
                f"\n\n<b>Состоит в клубе:</b> {player.club.name} (<code>{player.club.tag}</code>)"
                if player.club else ""
            ) + (
                "\n\n<b>Бойцы:</b>\n" + "\n".join(
                    f"    • <b>{brawler.name}:</b> сила {brawler.power}, ранг {brawler.rank}, троеев {brawler.trophies} (макс.: {brawler.highest_trophies})"
                    for brawler in player.brawlers
                ) if len(args) > 1 else ""
            )
        )

        return await utils.answer(
            message, f"<b>[BrawlStats]</b> Информацию о игроке:\n\n"
                     f"{text}"
        )

    async def bsclub_cmd(self, app: Client, message: types.Message, args: str):
        """Получить информацию о клубе. Использование: bsclub <тег> [любой аргумент - выведет только участников клуба]"""
        try:
            client = Client_(self.db.get("BrawlStats", "token", "дурак токен укажи"), is_async=True)
        except Forbidden:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Токен не указан или указан неверно")

        args = args.replace("#", "").upper().split()
        if not args:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Не указан тег игрока")

        try:
            club: Club = await client.get_club(args[0])
        except NotFoundError:
            return await utils.answer(
                message, "<b>[BrawlStats - Error]</b> Не удалось найти клуб")

        text = (
            f"<b>Название:</b> {club.name} (<code>{club.tag}</code>)\n" + (
                f"<b>Описание:</b> {club.description}\n"
                if club.description else ""
            ) + \
            f"<b>Участников:</b> {len(club.members)}\n"
            f"<b>Трофеи:</b> {club.trophies}" + (
                "\n\n<b>Участники:</b>\n" + "\n".join(
                    f"    • <b>{member.name}</b> (<code>{member.tag}</code>). Трофеев {member.trophies}"
                    for member in club.members
                ) if len(args) > 1 else ""
            )
        )

        return await utils.answer(
            message, f"<b>[BrawlStats]</b> Информацию о клубе:\n\n"
                     f"{text}"
        )
