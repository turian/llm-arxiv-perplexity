import glob
import re

BASE_DIR = "/Users/joseph/dev/HuggingFaceModelDownloader/"

general_pattern = re.compile(r'[0-9]-of-[0-9]')
exclusion_pattern = re.compile(r'00001-of-')

def find_all_gguf_models():
    gguf_models = glob.glob(BASE_DIR + "**/*gguf", recursive=True)
    for model in gguf_models:
        if general_pattern.search(model) and not exclusion_pattern.search(model):
             continue
        print(model)


if __name__ == "__main__":
    find_all_gguf_models()
