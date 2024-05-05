# llm-arxiv-perplexity
LLM perplexity on new arxiv papers

Predicting the future.

TODO:
* Should save the git hash of the model used (and llama.cpp version?)

Least surprised
Probably temporal validation of models is a good idea, for generalization

(How to do model selection, and folds)

Olmo

Outcome: Some outcomes are subjective, like which chatbot is the correct amount of supplicating.
Others, like the perplexity of important new research being low, it is hard to disagree that it is beneficial: We want LLMs that are minimally surprised by recent scientific developments, similar to how a top practitioner can audit new research quickly because they have a good command of the field's literature and a strong ability to predict the direction of the puck.

But, just finetuning an LLM at the end to minimize perplexity on an older corpus, that's a bit hmmm. I.e. finetuned ONLY to this measure and no other diverse fine-tuning datasets.

Issues with perplexity:
Honestly, used it because it was implemented in llama.cpp so I could experiment with a lot of different big models (quantized).
Current workflow for them is cat the documents. Issues:
* Can't find doc boundaries
* Can't macro average scores (and hard to macroaverage the error now)

Dataset creation
and issues therein, like html2text and only using /html/ arxiv.
Date and version.

Fine tuning on this task.

Better might be: Given the title, predict the perplexity of abstract.
Or just perplexity of title + abstract.


Predicting the news: Could also be economic, or political, or medical, etc news. A good world-model means that news should be less surprising.

If I found a model was promising, I would get more related models from the family, including fine-tunes and mashups from others. This could have been done in a more disciplined way, but honestly it's difficult to predict from a random huggingface model description how well it will do. (This is even show by some counter-intuitive results in the base models.)


Data contamination concerns:
* If it's a more recent version of something published before knowledge cutoff
* If it's published by a majro corp and they trained on the text before publishing

Related:
https://github.com/ggerganov/llama.cpp/discussions/2321
https://github.com/ggerganov/llama.cpp/issues/7066
https://github.com/bodaay/HuggingFaceModelDownloader/issues/30