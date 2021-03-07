class BaseRenderer:
  async def render(self, html: str, css: str, file_format: str):
    raise NotImplementedError()