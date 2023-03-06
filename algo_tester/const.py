from typing import TypedDict

DATASETS: list[str] = [
    "Bootstrap",
    "Camouflage",
    "ForegroundAperture",
    "LightSwitch",
    "MovedObject",
    "TimeOfDay",
    "WavingTrees"
]

ALGORITHMS: list[str] = [
    "IndependantMultimodal",
    "LBFuzzyGaussian",
    "LBMixtureOfGaussians",
    "LBSimpleGaussian",
    "SigmaDelta",
    "SuBSENSE",
    "T2FMRF-UV"
]


class Results(TypedDict):
    tn: int
    tp: int
    fn: int
    fp: int
    accuracy: float


class ImageResults(TypedDict):
    algo: str
    dataset: str
    results: Results


class AlgoStats(TypedDict):
    algo: str
    results: Results


class DatasetStats(TypedDict):
    dataset: str
    results: Results
