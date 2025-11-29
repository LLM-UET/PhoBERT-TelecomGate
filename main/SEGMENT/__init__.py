import csv
from ..data import (
    DEFAULT_RAW_PATH,
    DEFAULT_SEGMENTED_PATH,
)
from ..emo import process_emojis_and_emoticons_if_enabled

import requests

import os
RDRSEGMENTER_BASE_URL = os.getenv('RDRSEGMENTER_BASE_URL', 'http://localhost:8025')

def do_SEGMENT(input_file_path=None, output_file_path=None, silent=False):
    if silent:
        def PRINT(*args, **kwargs):
            pass
    else:
        PRINT = print

    ENCODING = 'utf-8-sig' # UTF-8 with BOM (EF BB BF)

    input_file_path = input_file_path or DEFAULT_RAW_PATH
    output_file_path = output_file_path or DEFAULT_SEGMENTED_PATH

    # ChatGPT:
    # Added newline='' in the CSV output file to avoid double blank lines on Windows.
    with open(output_file_path, 'w', encoding=ENCODING, newline='') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)

        with open(input_file_path, 'r', encoding=ENCODING) as input_file:
            reader = csv.reader(input_file)
            for row in reader:
                PRINT("Processing row:", row)
                text, label = row
                text = text.replace('\\n', '\n')

                segmented = segment_text_directly(text)

                writer.writerow((segmented, label))

        PRINT(f"Success. Output written to: {output_file_path}")

def segment_text_directly(text: str) -> str:
    text = process_emojis_and_emoticons_if_enabled(text)

    try:
        res = requests.post(
            f"{RDRSEGMENTER_BASE_URL}/v1/segment",
            data=text.encode('utf-8'),
            headers={'Content-Type': 'text/plain'}
        )
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Failed to connect to RDRsegmenter service at {RDRSEGMENTER_BASE_URL}. Ensure the service is running.") from e

    if not res.ok:
        raise RuntimeError(f"RDRsegmenter request failed with status code {res.status_code}: {res.text}")
    
    segmented = res.text.strip()
    return segmented
