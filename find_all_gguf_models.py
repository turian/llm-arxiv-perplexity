import glob
import re
import random

BASE_DIR = "/Users/joseph/dev/HuggingFaceModelDownloader/downloads/"

general_pattern = re.compile(r'[0-9]-of-[0-9]')
exclusion_pattern = re.compile(r'00001-of-')

def find_all_gguf_models():
    gguf_models = list(glob.glob(BASE_DIR + "**/*.gguf", recursive=True))
    random.seed(0)
    random.shuffle(gguf_models)
    for model in gguf_models:
        if general_pattern.search(model) and not exclusion_pattern.search(model):
             continue
        model_clean = model.replace(BASE_DIR, "")
        yield (model_clean, model)


if __name__ == "__main__":
    for m in find_all_gguf_models():
        print(m)
