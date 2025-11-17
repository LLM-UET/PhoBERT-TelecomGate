import re

EMOTICON_REGEX = {
    # Smiles
    r":\)+": "[smile_emoji]",          # :) :)) :))) etc.
    r":D+": "[grin_emoji]",            # :D, :DD
    r"=+\)+": "[smile_emoji]",         # =) or =))
    r">:\)+": "[evil_smile_emoji]",    # >:) etc.

    # Sad / frown
    r":\(+": "[sad_emoji]",            # :( :(( 
    r"=<\(+": "[sad_emoji]",           # =(
    r":'<+": "[cry_emoji]",            # :'<

    # Surprise / shock
    r":O+": "[surprise_emoji]",        # :O
    r":o+": "[surprise_emoji]",        # :o

    # Tongue / playful
    r":P+": "[tongue_emoji]",          # :P, :PP
    r":p+": "[tongue_emoji]",

    # Wink
    r";\)+": "[wink_emoji]",           # ;) ;))

    # Cute / other
    r":3+": "[cute_emoji]",
    r":>+": "[smirk_emoji]",
    r":<+": "[disappointed_emoji]",
    r":V+": "[peace_emoji]",            # :V
    r"XD+": "[laugh_emoji]",            # XD, XDD
    r"xD+": "[laugh_emoji]",
}

def process_emoticons(text: str) -> str:
    for pattern, repl in EMOTICON_REGEX.items():
        text = re.sub(pattern, repl, text)
    return text
