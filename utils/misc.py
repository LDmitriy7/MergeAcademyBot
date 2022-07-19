import re
from contextlib import suppress
from datetime import datetime


def uncapitalize(text: str):
    return text[0].lower() + text[1:]


def parse_phone(text: str):
    digits = ''.join(re.findall(r'\d', text))

    if len(digits) == 10:
        digits = '38' + digits

    if not len(digits) == 12:
        raise ValueError('Invalid phone number')

    return f'+{digits[:2]} ({digits[2:5]}) {digits[5:8]} {digits[8:10]} {digits[10:12]}'


def parse_post_date(text: str) -> int:
    for fmt in ['%d.%m.%y %H:%M', '%d.%m.%Y %H:%M']:
        with suppress(ValueError):
            dt = datetime.strptime(text, fmt)
            return int(dt.timestamp())
    raise ValueError('Invalid post date')


def safe_html(text: str) -> str:
    """Escape "<" and ">" symbols that are not a part of a tag."""
    return re.sub(
        pattern='<(?!(/|b>|i>|u>|s>|tg-spoiler>|a>|a href=|code>|pre>|code class=))',
        repl='&lt;',
        string=text,
    )
