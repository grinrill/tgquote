from .. import filegetters

from pathlib import Path

selfdir = Path(__file__).parent


class DebufFileGetter(filegetters.BaseFileGetter):
    async def get_file(self, file_id: str):
        return open(selfdir / file_id, 'rb')

    async def get_userpic(self, user_id: int):
        return open(selfdir / 'userpic.jpg', 'rb')

    async def get_thumb(self, message):
        return await self.get_document(message)

    async def get_document(self, message):
        """
        Тупой алгоритм,
        который рекурсивно с конца ищет поле "file_id"
        и если находит, возвращает имя его родителя
        + расширение в конце
        """
        if isinstance(message, list):
            values = list(enumerate(message))
        elif isinstance(message, dict):
            values = list(message.items())
        else:
            return
        values.reverse()

        for k, v in values:
            if k == 'reply_to_message':
                continue
            if isinstance(v, dict):
                if 'file_id' in v:
                    if k == 'sticker':
                        v['mime_type'] = (
                            'application/x-tgsticker'
                            if v['is_animated']
                            else 'img/webp'
                        )
                    v.update(
                        {
                            'file_id': k
                            + '.'
                            + (v.get('mime_type', 'img/jpg').split('/')[1])
                        }
                    )
                    return v
            if result := await self.get_document(v):
                return result
