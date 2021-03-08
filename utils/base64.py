import base64

def base64ToUrl(bytesio, mime_type):
  encoded = base64.b64encode(
    bytesio.read()
  )
  return f'data:{mime_type};base64, {encoded}'