class BaseFileGetter:
  async def get_file_by_file_id(self, file_id: str):
    raise NotImplementedError()

  async def get_file_by_message(self, message: dict):
    raise NotImplementedError()

  async def get_userpic_by_user_id(self, user_id: int):
    raise NotImplementedError()

  async def get_userpic_by_message(self, message: dict):
    raise NotImplementedError()