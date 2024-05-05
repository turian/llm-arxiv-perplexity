import glob
import gzip
import json
import re
from collections import defaultdict

ppl_re = re.compile("^Final estimate: PPL = ([0-9\.]+) ... ([0-9\.]+)$")

for date in glob.glob("data/*/"):
    thisdate = date.split("/")[-2]
    finalfile = f"{date}/final.jsonl"
    papers = []
    for paper in glob.glob(f"{date}/papers/*.txt"):
        thispaper = paper.split("/")[-1]
        papers.append(thispaper)

    model_to_paper = defaultdict(dict)
    for scorefile in glob.glob(f"{date}/models/*/*/*/perplexity.txt.gz"):
        thispaper = scorefile.split("/")[-4]
        model = tuple(scorefile.split("/")[-3:-1])
        with gzip.open(scorefile, "rt") as f:
            for l in f:
                if l.startswith("Final"):
                    m = ppl_re.match(l)
                    assert m
                    ppl = float(m.group(1))
                    ppl_err = float(m.group(2))
                    assert thispaper not in model_to_paper[model]
                    # model_to_paper[model][thispaper] = (ppl, ppl_err)
                    model_to_paper[model][thispaper] = ppl

    model_ppls = {}
    for model, thispapers in model_to_paper.items():
        if set(thispapers) == set(papers):
            ppl = sum(thispapers.values()) / len(thispapers)
            # print(ppl, thisdate, model)
            model_ppls[model] = ppl

    # Sort by increasing ppl
    model_ppls = {k: v for k, v in sorted(model_ppls.items(), key=lambda item: item[1])}

    """
    # Make a bar chart of the models, with logscale y
    import matplotlib.pyplot as plt
    import numpy as np


    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_yscale('log')
    ax.set_ylabel('PPL')
    ax.set_xlabel('Model')
    ax.set_title(f'PPL by model for {thisdate}')
    ax.bar([str(m[0]) for m in model_ppls], [ppl for ppl in model_ppls.values()])
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{thisdate}.png")
    """

    with open(finalfile, "wt") as f:
        for model, ppl in model_ppls.items():
            f.write(json.dumps({"model": model, "ppl": ppl}) + "\n")
