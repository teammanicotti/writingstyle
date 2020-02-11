"""
The Ensemble model pipeline.

Takes a collection of models, and if any model rejects a prediction
for a given token, then the pipeline will reject the prediction

Potentially, we could investigate returning a percentage of certainty?
I think we would need more models before we take this approach though.
"""


class EnsemblePipeline:

    def __init__(self, models):
        self.models = models

    def ensemble_predict(self, tokens):
        for model in self.models:
            if not model.predict(tokens):
                return False
        return True
