import aiohttp
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
import json

from .filegetter import DebufFileGetter
from .. import messages_to_html
from ..utils import templates_list, js

from pathlib import Path
selfdir = Path(__file__).parent
module = selfdir.parent

loader = FileSystemLoader(module/'templates')
env = Environment(
  loader=loader,
  enable_async=True,
  cache_size=0
)

filegetter = DebufFileGetter()

app = web.Application()
routes = web.RouteTableDef()

@routes.get('/')
async def debug(req: web.Request):
  messages = json.loads(
    open(selfdir/'messages.json').read()
  )
  css = open(module/'css/light.css').read()
  css += 'body {background-color: grey}'

  rendered = await messages_to_html(messages, env, files=filegetter, templates=templates_list)
  html = f'''
  <!!DOCTYPE html>
  <html>
    <head>
      <title>TelegramImage debug</title>
    </head>
    <body>
      <style>
      {css}
      </style>
      {rendered}
      <script src="https://oauth.tg.dev/js/telegram-widget.js?14"></script>
      <script src="https://tg.dev/js/tgsticker.js?24"></script>
      <script src="https://tg.dev/js/widget-frame.js?45"></script>
      '''+'''<script>
        TWidgetAuth.init({"api_url":"https:\/\/\/api\/method?api_hash=2e47378d2cf97fa915","upload_url":"https:\/\/\/api\/upload?api_hash=5d0c3cee1693c4e3be","unauth":true,"bot_id":1288099309});
        TWidgetPost.init();
        try{var a=new XMLHttpRequest;a.open("POST","");a.setRequestHeader("Content-type","application/x-www-form-urlencoded");a.send("_rl=1")}catch(e){}
      </script>
    </body>
  </html>
  '''
  return web.Response(body=html, content_type='text/html')

app.add_routes(routes)

if __name__ == '__main__':
  web.run_app(debug.app)