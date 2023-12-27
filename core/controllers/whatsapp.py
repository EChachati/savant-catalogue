from urllib.parse import quote


def link_generator(phone_number: str, text: str):
    phone_number.replace(" ", "").replace("+", "")
    text = quote(text)
    return f"https://api.whatsapp.com/send?phone={phone_number}&text={text}"
