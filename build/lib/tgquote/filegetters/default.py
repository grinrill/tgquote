from .base import BaseFileGetter
import io

import logging
logger = logging.getLogger(__file__)

class DefaultFileGetter(BaseFileGetter):
  def __init__(self, bot):
    self.bot = bot

  async def get_file(self, file_id: str):
    try:
      file_object = await self.bot.get_file(file_id)

      f = io.BytesIO()
      await file_object.download(f)
      return f
    except:
      logger.exception('get_file')
      return io.BytesIO(b'')

  # async def get_file_by_message(self, message: dict):
  #   """
  #   Тупой алгоритм,
  #   который рекурсивно с конца ищет поле "file_id"
  #   и если находит, возвращает с помощью метода get_file_by_file_id
  #   """
  #   if isinstance(message, list):
  #     values = list
  #   elif isinstance(message, dict):
  #     values = message.values()
  #   else: 
  #     return
  #   values.reverse()

  #   for i in values:
  #     if isinstance(i, dict):
  #       if 'file_id' in i:
  #         return await self.get_file_by_file_id(i['file_id'])
  #     if result := await self.get_file_by_message(i):
  #       return result

  async def get_userpic(self, user_id: int):
    try:
      if user_id > 0:
        file_object = await self.bot.get_user_profile_photos(
          user_id, 
          limit=1
        )
        f = io.BytesIO()    
        await file_object.photos[0][0].download(f)
        return f
      else:
        chat = await self.bot.get_chat(user_id)
        return await self.get_file(chat.small_file_id)
    except:
      logger.exception('get_userpic')
      return io.BytesIO(b'')

  # async def get_userpic_by_message(self, message: dict):
  #   if from_user := message.get('from'):
  #     return await self.get_userpic_by_user_id(from_user['id'])
  #   elif sender_chat := message.get('sender_chat'):
  #     chat = await self.bot.get_chat(sender_chat['id'])
  #     return await self.get_file_by_file_id(chat.small_file_id)