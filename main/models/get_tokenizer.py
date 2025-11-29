from .common import BASE_MODEL_DIR

# def get_tokenizer(model_dir=None, for_download=False):
#     from transformers import AutoTokenizer

#     if model_dir is None:
#         model_dir = BASE_MODEL_DIR

#     # if for_download:
#     #     tokenizer = AutoTokenizer.from_pretrained(
#     #         "vinai/phobert-base",
#     #         cache_dir=BASE_MODEL_DIR,
#     #     )
#     # else:
#     tokenizer = AutoTokenizer.from_pretrained(
#         "vinai/phobert-base",
#         cache_dir=model_dir,
#     )
    
#     return tokenizer


def get_tokenizer(model_dir: str | None = None, force_download: bool = False):
    """
    Load tokenizer, optionally forcing a behind-the-scenes download.
    """
    from transformers import AutoTokenizer
    from huggingface_hub import snapshot_download
    
    if model_dir is None:
        model_dir = BASE_MODEL_DIR

    if force_download:
        snapshot_download(
            repo_id="vinai/phobert-base",
            force_download=True,
            local_files_only=False,
            cache_dir=model_dir,
        )

    return AutoTokenizer.from_pretrained(model_dir)
