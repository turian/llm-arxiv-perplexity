import glob
import gzip
import re
from collections import Counter, defaultdict

features = ["model type", "model ftype", "model params", "model size", "general.name"]
feature_res = {
    feat: re.compile(f"^llm_load_print_meta: {feat} += (.*)$") for feat in features
}

model_feature_counts = {}
for f in glob.glob("data/*/models/*/*/*/perplexity.err.gz"):
    model = tuple(f.split("/")[-3:-1])
    if model not in model_feature_counts:
        model_feature_counts[model] = {feat: Counter() for feat in features}
    with gzip.open(f, "rt") as f:
        for l in f:
            for feat, fre in feature_res.items():
                if fre.match(l):
                    model_feature_counts[model][feat].update([fre.match(l).group(1)])

for model in model_feature_counts:
    for feat in features:
        print(model, feat, model_feature_counts[model][feat])
