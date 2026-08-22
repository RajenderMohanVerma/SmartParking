from io import BytesIO

import qrcode


def make_qr(token):
    image = qrcode.make(token)
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output
