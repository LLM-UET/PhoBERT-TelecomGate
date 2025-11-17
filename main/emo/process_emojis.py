import emoji

def process_emojis(text: str) -> str:
    return emoji.demojize(text, delimiters=("[", "]"))
