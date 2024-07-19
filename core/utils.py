import datetime
import qrcode
from io import BytesIO
from django.core.files import File


def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None


def format_date(date):
    return date.strftime('%Y-%m-%d')


def apply_filters(queryset, filters):
    for key, value in filters.items():
        if value is not None:
            queryset = queryset.filter(**{key: value})
    return queryset


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return File(byte_io, name=f'{data}.png')
