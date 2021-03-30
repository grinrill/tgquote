import typing
import io

try:
  from aiogram import Bot
except ModuleNotFoundError:
  Bot = None

class MediaFile:
  def __init__(
    self,
    bot: Bot = None,
    file_id: str = None,
    file_unique_id: str = None,
    file: typing.Union[str, io.BytesIO] = None,
    file_name: str = None,
    file_size: int = None,
    file_object = None,
  ):
    self.file_id = file_id
    self.file_name = file_name
    self.file_size = file_size
    self.file = file
    self.downloaded = bool(file)

  async def get_file(self):
    if isinstance(self.file, io.BytesIO):
      return self.file
    if isinstance(self.file, str):
      return open(self.file)
    

class MediaUserpic(MediaFile):
  def __init__(
    self,
    user_id: int,
    file_id: str = None,
    file: typing.Union[str, io.BytesIO] = None,
    file_name: str = None,
    file_size: int = None,
  ):
    self.user_id = user_id
    super().__init__(file_id,
                     file, 
                     file_name,
                     file_size,)

class Media:
  files: typing.Dict[str, MediaFile]
  userpics: typing.Dict[int, MediaUserpic]

  def __init__(
    self,
    files: typing.Dict[str, MediaFile] = None,
    userpics: typing.Dict[int, MediaUserpic] = None,
    bot: Bot = None,
  ):
    if files is None:
      files = {}
    if userpics is None:
      userpics = {}

    self.files = files
    self.userpics = userpics
    self.bot = bot

  def add_file(self, file):
    if hasattr(file, 'user_id'):
      self.userpics[file.user_id] = file
    if hasattr(file, 'file_id'):
      self.files[file.file_id] = file
    if hasattr(file, 'file_unique_id'):
      self.files[file.file_unique_id] = file

  def get_file(
    self, 
    file_id: typing.Union[int, str] = None,
    user_id: int = None,
    file_unique_id: str = None, 
  ):
    if not any((file_id, file_unique_id)):
      raise ValueError('Required one of user_id, '
                       'file_id or file_unique_id')
    
    if isinstance(file_id, int):
      user_id = file_id

    if user_id:
      return self.userpics.get(user_id)
    if file_id or file_unique_id:
      return self.files.get(file_id or file_unique_id)
  
  async def download_files(self, bot=None):
    if not bot:
      bot = self.bot
    
    if bot is None:
      raise ValueError('To download files, a bot object required. '
                       'The files will not be downloaded automatically.')

    for file in self.files:
      if file.downloaded:
        continue
      if not file.file_id:
        continue
        
      file.file = io.BytesIO()
      if not file.file_object:
        file.file_object = await bot.get_file(file.file_id)
      await file.file_object.download(file.file)

    for photo in self.userpics:
      if photo.downloaded:
        continue
      
      photo.file = io.BytesIO()
      if not photo.file_object:
        photo.file_object = await bot.get_user_profile_photos(
          file.user_id, 
          limit=1
          )
      await photo.file_object.photos[0][0].download(file.file)
      
      
