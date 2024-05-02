# Prediction interface for Cog ⚙️
# https://cog.run/python

import os
from cog import BasePredictor, Input, Path
import tempfile


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        hfmodel: str = Input(description="HuggingFace organization/model name"),
        hffilter: str = Input(
            description="Filter, e.g. Q5_K_M", default="Q5_K_M"
        ),
    ) -> Path:
        """Run a single prediction on the model"""
        assert hfmodel is not None and hfmodel != ""
        assert hffilter is not None and hffilter != ""
        #cmd = f"bash <(curl -sSL https://g.bodaay.io/hfd) -m {hfmodel}:{hffilter}"
        cmd = f"bash -c 'bash <(curl -sSL https://g.bodaay.io/hfd) -m {hfmodel}:{hffilter}'"
        print(cmd)
        os.system(cmd)
        cmd = f"python3 score-all.py"
        print(cmd)
        os.system(cmd)

        # This gets deleted after we run
        output_path = Path(tempfile.mkdtemp()) / "output.tar.gz"

        cmd = f"tar zcvf {output_path} data/*/models"
        print(cmd)
        os.system(cmd)
        return output_path
