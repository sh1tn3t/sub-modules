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

# required: wand pillow

import io
import tempfile

from wand.image import Image as WandImage
from PIL import Image as PILImage

from pyrogram import Client, types
from .. import loader, utils


def distort(image: io.BytesIO, rescale_rate: int) -> io.BytesIO:
    img = WandImage(file=image)
    x, y = img.size[0], img.size[1]

    pop_x = int(rescale_rate * (x // 100))
    pop_y = int(rescale_rate * (y // 100))

    img.liquid_rescale(pop_x, pop_y, delta_x=1, rigidity=0)
    img.resize(x, y)

    out = io.BytesIO()
    out.name = "output.png"
    img.save(file=out)

    return io.BytesIO(out.getvalue())


@loader.module("Distort", "sh1tn3t")
class DistortMod(loader.Module):
    """Сжатие изображения"""

    async def distort_cmd(self, app: Client, message: types.Message, args: str):
        """Сжать изображение. Использование: distort <реплай на фото или стикер> [% сжатия от 1 до 99]"""
        reply = message.reply_to_message
        file = (           
            reply.photo
            if reply.photo
            else reply.sticker
            if reply.sticker and not reply.sticker.is_animated
            else None
        )
        if not file:
            return await utils.answer(
                message, "<b>[Distort]</b> Нет реплая на фото или стикер")

        distort_rate = (
            int(args)
            if args and args.isdigit() and 0 < int(args) < 100
            else 35
        )

        await utils.answer(
            message, "<b>[Distort]</b> Скачиваю...")

        temp_file = tempfile.NamedTemporaryFile("w")
        await reply.download(temp_file.name)

        await utils.answer(
            message, "<b>[Distort]</b> Сжимаю...")

        image = io.BytesIO()
        image.name = "image.png"

        file = io.BytesIO(open(temp_file.name, "rb").read())
        PILImage.open(file).save(image, 'PNG')

        media = distort(io.BytesIO(image.getvalue()), 100 - distort_rate)
        out, im = io.BytesIO(), PILImage.open(media)

        out.name = "out.png"
        im.save(out, "PNG")
        out.seek(0)

        await utils.answer(
            message, "<b>[Distort]</b> Отправляю...")

        await utils.answer(
            message, out, photo=True)
        return await message.delete()
