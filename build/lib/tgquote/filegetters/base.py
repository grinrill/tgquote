class BaseFileGetter:
  async def get_file(self, file_id: str):
    raise NotImplementedError()

  async def get_userpic(self, user_id: int):
    raise NotImplementedError()

  async def get_thumb(self, message):
    """
    Тупой алгоритм,
    который рекурсивно с конца ищет поле "thumb"
    и если находит, возвращает его
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
        if 'thumb' in v:
          return v['thumb']
      if result := await self.get_thumb(v):
        return result

  async def get_document(self, message):
    """
    Тупой алгоритм,
    который рекурсивно с конца ищет поле "file_id"
    и если находит, возвращает его родителя
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
          return v
      if result := await self.get_document(v):
        return result