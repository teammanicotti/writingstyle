class EnsemblePipeline:

    def __init__(self, models):
        self.models = models

    def ensemble_predict(self, tokens):
        print(self.models)
        for model in self.models:
            if not model.predict(tokens):
                return False
        return True
