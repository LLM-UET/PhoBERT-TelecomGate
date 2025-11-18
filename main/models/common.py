import os

BASE_MODEL_DIR = os.getenv("BASE_MODEL_DIR", "./models/phobert-base-local/models--vinai--phobert-base/snapshots/c1e37c5c86f918761049cef6fa216b4779d0d01d")

FINETUNED_MODEL_DIR = os.getenv("FINETUNED_MODEL_DIR", "./models/finetuned")

LABELS = ['Negative', 'Neutral', 'Positive']

NUM_LABELS = len(LABELS)

LABEL_TO_ID = {label: i for i, label in enumerate(LABELS)}

ID_TO_LABEL = {i: label for i, label in enumerate(LABELS)}
