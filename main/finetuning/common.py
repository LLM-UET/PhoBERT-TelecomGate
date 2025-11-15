import os

# Maximum length of an input sequence after tokenization
MAX_LEN = 128

BATCH_SIZE = 8 # for 16GB GPU, fp32

NUM_EPOCHS = int(os.getenv("NUM_EPOCHS", 3))

LEARNING_RATE = 2e-5
