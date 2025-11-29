def do_DOWNLOAD_MODELS_BASE():
    from ..models import get_tokenizer, get_classifier

    tokenizer = get_tokenizer(force_download=True)
    get_classifier = get_classifier(force_download=True)

    return (tokenizer, get_classifier)

def do_DOWNLOAD_MODELS_FINETUNED():
    from ..models import FINETUNED_MODEL_DIR
    import os
    import time

    TEMP_KAGGLE_OUTPUT_PATH = os.path.join(
        os.path.dirname(
            FINETUNED_MODEL_DIR.strip("/")
        ),
        f"temp_kaggle_download_{int(time.time())}",
    )

    import subprocess

    # https://www.kaggle.com/code/laamegg/phobert-telecomgate-finetuning
    # kaggle kernels output laamegg/phobert-telecomgate-finetuning -p /path/to/dest
    try:
        subprocess.run(
            [
                "kaggle",
                "kernels",
                "output",
                "laamegg/phobert-telecomgate-finetuning",
                "-p",
                TEMP_KAGGLE_OUTPUT_PATH,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Kaggle command failed with exit code {e.returncode}"
        )
    
    import shutil
    if os.path.exists(FINETUNED_MODEL_DIR):
        print(f"Removing existing finetuned model directory: {FINETUNED_MODEL_DIR}")
        shutil.rmtree(FINETUNED_MODEL_DIR)
    print(f"Moving the downloaded models to {FINETUNED_MODEL_DIR}")
    shutil.move(
        os.path.join(
            TEMP_KAGGLE_OUTPUT_PATH, "finetuned",
        ),
        FINETUNED_MODEL_DIR,
    )
    print(f"Cleaning up temporary directory: {TEMP_KAGGLE_OUTPUT_PATH}")
    shutil.rmtree(TEMP_KAGGLE_OUTPUT_PATH)
    print(f"Quick check the downloaded files...")
    for file_name in ["config.json", "training_args.bin", "tokenizer_config.json", "vocab.txt", "model.safetensors", "bpe.codes"]:
        assert file_name in os.listdir(FINETUNED_MODEL_DIR), f"File {file_name} not found in {FINETUNED_MODEL_DIR}"
    
    print(f"FINETUNED models downloaded successfully to {FINETUNED_MODEL_DIR}")
