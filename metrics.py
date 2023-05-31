from abc import ABC, abstractclassmethod

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from functools import partial
from data.loader import Dataset


class Metric(ABC):
    @abstractclassmethod
    def __call__(self, estimator, dataset: Dataset):
        pass


class CrossValidation(Metric):
    def __init__(self, scoring, **kwargs):
        self.scoring = partial(scoring, **kwargs)
        self.name = f'Cross Validation, scoring {scoring.__name__}'
        params = ', '.join([f'{name} {value}' for name, value in kwargs.items()])
        if params:
            self.name += f' with {params}'
    
    def __call__(self, *args):
        estimator, dataset = args

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', estimator)
        ])
        
        return cross_val_score(pipeline, dataset.features, dataset.targets, scoring=self.get_score).mean()
    
    def get_score(self, *args):
        estimator, features, targets = args
        return self.scoring(targets, estimator.predict(features))
