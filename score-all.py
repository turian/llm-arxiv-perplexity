import datetime
import glob
import json
import os.path
import random
import tempfile

from tqdm import tqdm

from find_all_gguf_models import find_all_gguf_models

random.seed(0)

papers = sorted(list(glob.glob("data/*/papers/*.txt")))
random.shuffle(papers)

models = list(find_all_gguf_models())

paper_model_pairs = []
for paper in papers:
    for model_clean, model in models:
        model_output = os.path.join(
            paper.replace("papers", "models"), model_clean, "perplexity.txt"
        )
        if os.path.exists(model_output):
            continue
        paper_model_pairs.append((paper, model, model_clean, model_output))

for paper, model, model_clean, model_output in tqdm(paper_model_pairs):
    print(f"Processing {paper} with {model_clean}")
    os.makedirs(os.path.dirname(model_output), exist_ok=True)
    if os.path.exists(model_output):
        continue

    # Create named temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create temporary file
        tmptxtfile = os.path.join(tmpdirname, "tmp.txt")
        tmperrfile = os.path.join(tmpdirname, "tmp.err")
        # Run perplexity
        cmd = f"CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 /llama.cpp/build/bin/perplexity --model {model} -f {paper} --flash-attn --seed 0 -ngl 128 > {tmptxtfile} 2> {tmperrfile}"
        print(cmd)
        now = datetime.datetime.now()
        os.system(cmd)

        if "Final estimate" not in open(tmptxtfile).read():
            print(f"Final estimate not found in {tmptxtfile}")
            print(open(tmptxtfile).read())
            print(open(tmperrfile).read())
            continue

        elapsed = datetime.datetime.now() - now

        finaltxtfile = model_output
        assert finaltxtfile.endswith(".txt")
        finalerrfile = finaltxtfile[:-4] + ".err"
        os.rename(tmperrfile, finalerrfile)
        os.rename(tmptxtfile, finaltxtfile)
        finalerrfile = finaltxtfile[:-4] + ".json"
        with open(finalerrfile, "wt") as f:
            f.write(
                json.dumps(
                    {
                        "elapsed": elapsed.total_seconds(),
                        "model": model,
                        "paper": paper,
                        "model_clean": model_clean,
                    }
                )
            )
