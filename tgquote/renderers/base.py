import typing
import io


class BaseRenderer:
    async def render(
        self,
        html: str,
        css: str,
        file_format: str,
        file: typing.Union[str, io.BytesIO] = None,
    ):
        raise NotImplementedError()

    async def close(self):
        pass
