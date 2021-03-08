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
      values = list
    elif isinstance(message, dict):
      values = list(message.values())
    else: 
      return
    values.reverse()

    for i in values:
      if isinstance(i, dict):
        if 'thumb' in i:
          return i['thumb']
      if result := await self.get_thumb(i):
        return result

  async def get_document(self, message):
    """
    Тупой алгоритм,
    который рекурсивно с конца ищет поле "file_id"
    и если находит, возвращает его родителя
    """
    if isinstance(message, list):
      values = list
    elif isinstance(message, dict):
      values = list(message.values())
    else: 
      return
    values.reverse()

    for i in values:
      if isinstance(i, dict):
        if 'file_id' in i:
          return i
      if result := await self.get_document(i):
        return result