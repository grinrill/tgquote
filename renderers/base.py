class BaseRenderer:
  async def render(self, html: str, styles: str, image_type: str):
    raise NotImplementedError()