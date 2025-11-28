# PhoBERT Finetuning for Telecom-Domain Input Classification

- [PhoBERT Finetuning for Telecom-Domain Input Classification](#phobert-finetuning-for-telecom-domain-input-classification)
  - [Foreword](#foreword)
  - [Docker](#docker)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Prepare the Python environment](#prepare-the-python-environment)
    - [Downloading the Models](#downloading-the-models)
    - [Download RDRsegmenter JAR into project root](#download-rdrsegmenter-jar-into-project-root)
    - [Run the RDRsegmenter TXT-RPC server](#run-the-rdrsegmenter-txt-rpc-server)
    - [Setup Environment Variables](#setup-environment-variables)
  - [Prepare the Datasets](#prepare-the-datasets)
  - [Input Segmentation](#input-segmentation)
  - [Data Splitting](#data-splitting)
  - [Finetuning](#finetuning)
  - [Inference](#inference)
  - [RPC Server](#rpc-server)
  - [References](#references)

## Foreword

**IF YOU JUST WANT INFERENCE**, there are two options:

1. **Running in Docker:** Simple, quick.
   
    Follow the instructions in:
   
    - [Docker](#docker)

2. **Running directly:** For development and testing.
   
    Follow the instructions in:

    - [Setup](#setup)
    - [Inference](#inference)
    - and optionally [RPC Server](#rpc-server)

## Docker

1. Install Docker.

2. Log in to your Kaggle account and obtain the credentials JSON file,
    [as instructed here](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md#api-credentials).
    
    (Don't worry, the credentials are temporary
    and won't be baked into the built images.)

3. Open that JSON file, copy the values of
    `username` and `key`.

4. In this project's root:

    ```sh
    cp docker.env.example docker.env
    ```

5. Modify the variables inside the `docker.env`
    file, pasting the copied values to appropriate
    variables.

6. Run (still in project root):

    ```sh
    DOCKER_BUILDKIT=1 \
    COMPOSE_DOCKER_CLI_BUILD=1 \
    docker compose build --parallel
    ```

7. Now that the images are built, you could run
    them:

    ```sh
    docker compose up
    ```

    After that, you could access the RPC
    server at base URL `http://localhost:8135`.

[Here is the information on how to use the RPC server](#rpc-server)
(no need to run the commands in that section,
just see how to `curl` the server).

## Setup

### Prerequisites

- Python 3.12+
- Java 1.8+
- Kaggle CLI

### Prepare the Python environment

```sh
uv venv
source .venv/bin/activate
uv sync
```

### Downloading the Models

- **Base models** (not finetuned):

    ```sh
    source .venv/bin/activate
    uv run -m main download models BASE
    ```

    If you run the above commands
    twice, the models would not be
    downloaded again (i.e. it
    guarantees idempotency).

- **Finetuned models**:

    ```sh
    source .venv/bin/activate
    uv run -m main download models FINETUNED
    ```

    Beware, though, that this command is
    NOT idempotent. Running it the second
    time means re-downloading the models.

### Download RDRsegmenter JAR into project root
  
```sh
curl -L -O https://github.com/LLM-UET/RDRsegmenter/releases/download/0.9.1/RDRsegmenter.jar
```

Checksumming:

```sh
echo "47d3581e050bd686b9eac4727d4d453a5458d6b843e9b3c618a23f3654bdd7fa  RDRsegmenter.jar" | sha256sum --check
```

### Run the RDRsegmenter TXT-RPC server

This is required so that some stuff
could use RDRsegmenter via text RPC
(simple HTTP POST) to segment data,
as you would see later.

```sh
java -jar RDRsegmenter.jar TXT-RPC
```

or, to customize port:

```sh
java -jar RDRsegmenter.jar TXT-RPC 8025
```

### Setup Environment Variables

```sh
cp .env.example .env
```

then edit the variables in `.env`.

## Prepare the Datasets

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

## Data Splitting

You must split `segmented.csv` into `train.csv`,
`cv.csv`, and `test.csv`.

To do that automatically:

```sh
source .venv/bin/activate
uv run -m main split
```

## Finetuning

```sh
source .venv/bin/activate
uv run -m main finetune
```

## Inference

```sh
source .venv/bin/activate
uv run -m main infer "text to infer"
```

**The input text must NOT be segmented.**

You can use `\n` to denote newlines inside
the input text string.

Output will be printed directly to `stdout`.

For interactive use (the downside: you
cannot insert newlines as input, even `\n` ;
pressing Enter means another query):

```sh
source .venv/bin/activate
uv run -m main infer --interactive
```

To change the model used for inference, pass
`--input-model-dir=/path/to/model`. Hint
(assuming you've [downloaded the necessary models](#downloading-the-models),
be it BASE, FINETUNED, or both):

- By default, it uses the FINETUNED model.
- To use BASE instead: pass the path `./models/phobert-base-local`.

## RPC Server

Currently the server only exposes
the Inference API.

```sh
source .venv/bin/activate
uv run -m main serve
```

Add `--port=XXXX` if you want it
to listen at a different port.

Test (for default port at localhost):

```sh
curl http://localhost:8135/v1/infer --http1.1 -X POST -H 'Content-Type: text/plain' -d 'Xin chào các bạn yêu quý! Chúng tôi rất trân trọng tình cảm của các bạn...
Hôm nay mọi người có vui không ạ?
Hãy cho phép tôi được giới thiệu bản thân nhé!'
```

which should output `Positive`. Or:

```sh
curl http://localhost:8135/v1/infer --http1.1 -X POST -H 'Content-Type: text/plain' -d 'Làm ăn cái kiểu gì đấy hả?'
```

which should output `Negative`. Or:

```sh
curl http://localhost:8135/v1/infer --http1.1 -X POST -H 'Content-Type: text/plain' -d 'Ừ anh biết rồi, nói chung cũng tạm được :>'
```

which should output `Neutral` (or `Positive`, depending on training set). Or:

```sh
curl -s --write-out "\n\n<<< HTTP Code: %{http_code} >>>\n" http://localhost:8135/v1/infer --http1.1 -X POST
```

which should output:

    No input text?

    <<< HTTP Code: 400 >>>

The protocol is, you expect to get 200 and response
body `Positive`, `Negative`, `Neutral`; or some
other code, in which case the response body
contains the error message.

## References

    @inproceedings{phobert,
    title     = {{PhoBERT: Pre-trained language models for Vietnamese}},
    author    = {Dat Quoc Nguyen and Anh Tuan Nguyen},
    booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2020},
    year      = {2020},
    pages     = {1037--1042}
    }
