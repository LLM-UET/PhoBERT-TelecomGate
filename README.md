# PhoBERT Finetuning for Sentiment Classification

- [PhoBERT Finetuning for Sentiment Classification](#phobert-finetuning-for-sentiment-classification)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Input Segmentation](#input-segmentation)
  - [Downloading the Model](#downloading-the-model)

## Prerequisites

- Python 3.12+
- Java 1.8+

## Setup

- Prepare the Python environment:

    ```sh
    uv venv
    source .venv/bin/activate
    uv sync
    ```

- Download RDRsegmenter JAR into the project
    root:
  
    ```sh
    curl -L -O https://github.com/LLM-UET/RDRsegmenter/releases/download/0.9.0/RDRsegmenter.jar
    ```

    Checksumming:

    ```sh
    echo "a59636ec2ef9d1963d10d8c7a4033a710d606250b4c35949c519b059a6ab99a4  RDRsegmenter.jar" | sha256sum --check
    ```

- Prepare the datasets:

    - Datasets must be CSV files, **without headers**,
      consisting of `text,label` entries.

    - It is highly recommended that the `text` part
      be wrapped in a pair of double quotes (`""`)
      to prevent incorrect parsing that stems from
      commas inside `text`.

    - Example entries in a dataset file:
    
          ```csv
          "Nạp tiền mà sao chưa thấy vào tài khoản?",Negative
          "Gói Mimax70 có ổn không?",Neutral
          "Sao hủy gói F90 không được nhỉ",Negative
          "Data dùng tẹt ga luôn ^^",Positive
          ```
    
    - Place a dataset file named `data.csv`
      under directory `<project_root>/datasets`.
      The app will split it into train/cv/test
      sets automatically and deterministically
      with a fixed seed.
    
    - Before proceeding, **make sure the CSV file(s)**
      **do NOT contain "smart quotes"**, i.e. search
      for the following quotes: `“` and `”` and
      remove them both with normal double quotes `"`.
    
    - Also watch out for open/unclosed/lone quotes,
      e.g. `"Have you finished this sentence yet,Negative`.

## Input Segmentation

If you've already done it with
`data.csv`, copy `data.csv` into a new
file named `segmented.csv`, under the
same directory.

Otherwise, run:

```sh
source .venv/bin/activate
uv run -m main segment
```

**It will output to `segmented.csv`** under the
same directory as `data.csv`.

**It should not be run more than once**
since `segment(segment(text)) != segment(text)`.

## Downloading the Model

```sh
source .venv/bin/activate
uv run -m main download models
```
