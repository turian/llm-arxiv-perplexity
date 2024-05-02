import glob

BASE_DIR = "/Users/joseph/dev/HuggingFaceModelDownloader/"


def find_all_gguf_models():
    gguf_models = glob.glob(BASE_DIR + "**/*gguf", recursive=True)
    for model in gguf_models:
        print(model)


if __name__ == "__main__":
    find_all_gguf_models()
