import glob
import random
import os.path
from tqdm import tqdm
import tempfile

from find_all_gguf_models import find_all_gguf_models

random.seed(0)

papers = list(glob.glob("data/*/papers/*.txt"))
random.shuffle(papers)

models = list(find_all_gguf_models())

paper_model_pairs = []
for paper in papers:
    for (model_clean, model) in models:
        model_output = os.path.join(paper.replace("papers", "models"), model_clean, "perplexity.txt")
        if os.path.exists(model_output):
            continue
        paper_model_pairs.append((paper, model, model_clean, model_output))

for (paper, model, model_clean, model_output) in tqdm(paper_model_pairs):
    print(f"Processing {paper} with {model_clean}")
    os.makedirs(os.path.dirname(model_output), exist_ok=True)

    # Create named temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create temporary file
        tmptxtfile = os.path.join(tmpdirname, "tmp.txt")
        tmperrfile = os.path.join(tmpdirname, "tmp.err")
        # Run perplexity
        cmd = f"/Users/joseph/dev/llama.cpp/perplexity --model {model} -f {paper} --flash-attn --seed 0 > {tmptxtfile} 2> {tmperrfile}"
        os.system(cmd)

        if "Final estimate" not in open(tmperrfile).read():
            continue

        finaltxtfile = model_output
        assert finaltxtfile.endswith(".txt")
        finalerrfile = finaltxtfile[:-4] + ".err"
        os.rename(tmperrfile, finalerrfile)
        os.rename(tmptxtfile, finaltxtfile)