from datasets import load_dataset, Features, Value

def load_csv_dataset(file_path, column_names=["text", "label"]):
    # Force every column to be string
    features = Features({
        col: Value("string") for col in column_names
    })

    dataset = load_dataset(
        "csv",
        data_files=file_path,
        column_names=column_names,
        features=features,  # <-- prevents dtype inference
    )
    
    dataset = dataset["train"] # type: ignore

    return dataset

def load_many_csv_datasets(file_paths, column_names=["text", "label"]):
    # Force every column to be string
    features = Features({
        col: Value("string") for col in column_names
    })

    dataset = load_dataset(
        "csv",
        data_files=file_paths,
        column_names=column_names,
        features=features,
    )

    return dataset
