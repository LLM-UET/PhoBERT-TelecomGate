from .common import MODEL_DIR

def get_tokenizer(force_download=False):
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        "vinai/phobert-base",
        cache_dir=MODEL_DIR,
        force_download=force_download,
    )
    
    return tokenizer
