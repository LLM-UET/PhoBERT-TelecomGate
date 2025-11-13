import csv
import subprocess

def do_SEGMENT(input_file_path=None, output_file_path=None):
    ENCODING = 'utf-8-sig' # UTF-8 with BOM (EF BB BF)
    RDRSEGMENTER_COMMAND = ["java", "-jar", "RDRsegmenter.jar", "STDIN"]

    input_file_path = input_file_path or "./datasets/data.csv"
    output_file_path = output_file_path or "./datasets/segmented.csv"

    # ChatGPT:
    # Added newline='' in the CSV output file to avoid double blank lines on Windows.
    with open(output_file_path, 'w', encoding=ENCODING, newline='') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)

        proc = subprocess.Popen(
            RDRSEGMENTER_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,           # handle text instead of bytes
            bufsize=1            # line-buffered I/O
        )

        try:
            with open(input_file_path, 'r', encoding=ENCODING) as input_file:
                reader = csv.reader(input_file)
                for row in reader:
                    print("Processing row:", row)
                    text, label = row
                    text = text.replace('\\n', '\n')

                    num_text_lines = len(text.split('\n'))
                    proc.stdin.write(text + '\n')
                    proc.stdin.flush()

                    segmented_lines: list[str] = []
                    for i in range(num_text_lines):
                        segmented_line = proc.stdout.readline().strip()
                        if not segmented_line:
                            raise RuntimeError("RDRsegmenter terminated unexpectedly")
                        segmented_lines.append(segmented_line)

                    segmented = '\\n'.join(segmented_lines)

                    writer.writerow((segmented, label))
        finally:
            proc.stdin.close()
            
            stderr = proc.stderr.read()
            ret = proc.wait()
        
    if ret != 0:
        print("RDRsegmenter failed with code", ret)
        print(stderr)
    else:
        print(f"Success. Output written to: {output_file_path}")
