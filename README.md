# telegramimage
Python module for screenshoting telegram messages.

## Example
``` python3
from telegramimage import TelegramImageRenderer
from telegramimage.renderers import HtmlCssToImageRenderer
from telegramimage.filegetters import DefaultFileGetter


from aiogram import Bot, Dispatcher, executor, types
bot = Bot('your bot token')
dp = Dispatcher(bot)

quoter = TelegramImageRenderer(
  HtmlCssToImageRenderer(
    api_id = 'your htmlcsstoimage.com api_id',
    api_key = 'your htmlcsstoimage.com api_key',
    api_url='https://htmlcsstoimage.com/demo_run'
    # I use demo apis for tests
    # I DO NOT RECOMMEND using the demo api in the prod
  ),
  DefaultFileGetter(bot),
  append_styles='body {background-color: grey}',
  # by default background is transparent
)


@dp.message_handler(
  content_types=types.ContentTypes.ANY
)
async def handler(message):
  await message.chat.do('upload_photo')
  f = await quoter.render(message)
  await message.reply_photo(f)
  
executor.start_polling(dp, skip_updates=True)
```
