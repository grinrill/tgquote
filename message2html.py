from jinja2 import Environment, FileSystemLoader
from jinja2 import Environment, FileSystemLoader
from .filegetters import BaseFileGetter
from . import utils
import typing

env = Environment(
    loader=FileSystemLoader('./templates'),
    enable_async=True,
)


async def messagesToHtml(
    messages: typing.List[dict],
    filegetter: BaseFileGetter,
    env: Environment = env,
  ):
  template = env.get_template('index.jinja2')

  html = await template.render_async(
    messages = messages,
    files = filegetter,
    utils = utils,
  )
  return html