from .common import BASE_MODEL_DIR, NUM_LABELS

# def get_classifier(model_dir=None, for_download=False):
#     from transformers import AutoModelForSequenceClassification

#     if model_dir is None:
#         model_dir = BASE_MODEL_DIR

#     # if for_download:
#     #     model = AutoModelForSequenceClassification.from_pretrained(
#     #         "vinai/phobert-base",
#     #         num_labels=NUM_LABELS,
#     #         cache_dir=BASE_MODEL_DIR,
#     #     )
#     # else:
#     model = AutoModelForSequenceClassification.from_pretrained(
#         "vinai/phobert-base",
#         num_labels=NUM_LABELS,
#         cache_dir=model_dir,
#     )
    
#     return model

def get_classifier(model_dir=None, force_download: bool = False):
    """
    Load classifier, optionally forcing a behind-the-scenes download.
    """
    from transformers import AutoModelForSequenceClassification
    from huggingface_hub import snapshot_download

    if model_dir is None:
        model_dir = BASE_MODEL_DIR

    if force_download:
        snapshot_download(
            repo_id="vinai/phobert-base",
            # force_download=True,
            local_files_only=False,
            cache_dir=model_dir,
        )
    return AutoModelForSequenceClassification.from_pretrained(model_dir, num_labels=NUM_LABELS)
