from .common import MODEL_DIR, NUM_LABELS

def get_classifier(force_download=False):
    from transformers import AutoModelForSequenceClassification

    model = AutoModelForSequenceClassification.from_pretrained(
        "vinai/phobert-base",
        num_labels=NUM_LABELS,
        cache_dir=MODEL_DIR,
        force_download=force_download,
    )
    
    return model
