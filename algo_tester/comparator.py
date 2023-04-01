from algo_tester.types import *
import os
import statistics
from PIL import Image
# https://pillow.readthedocs.io/en/stable/handbook/tutorial.html


class Comparator():

    '''
    Class taking a set of pictures (processed by algorithm) and comparing
    them to some ground truths (references). The goal is to determine the
    accuracy and the efficiency of the different movement detection
    algorithms.
    '''

    def __init__(self, directory: str) -> None:
        self._directory: str = directory
        self._files: list[str] = os.listdir(directory)
        self._groundtruths: list[str] = []
        self._files_to_analyze: list[str] = []
        self._images_results: list[ImageResults] = []
        self._algos_results: AlgoResults = {}
        self._algos_stats: list[AlgoStats] = []
        self._datasets_results: DatasetResults = {}
        self._datasets_stats: list[DatasetStats] = []
    
    def start(self):

        '''Public function to call first, starting the machine'''

        self._init_lists()
        self._compute_comparisons()
        self._compute_algos_stats()
        self._compute_datasets_stats()

    def _init_lists(self):

        '''Generating lists of the different algorithms and dataset provided'''

        for filename in self._files:
            file_details: list[str] = filename.split('_')

            if file_details[0] == "":
                continue
            elif file_details[0] == "GroundTruth":
                self._groundtruths.append(filename)
                continue
            elif file_details[0] in ALGORITHMS:
                self._files_to_analyze.append(filename)
            else:
                print(f'{filename} : filename not formatted as expected')
        
        for algo in ALGORITHMS:
            self._algos_results[algo] = []
        
        for dataset in DATASETS:
            self._datasets_results[dataset] = []

    def _compute_comparisons(self):

        '''Method processing all the pictures provided in the folder'''

        for filename in self._files_to_analyze:
            algo, dataset, *_ = filename.split('_')
            groundtruth_file: str = ""

            for value in self._groundtruths:
                if value.find(dataset) != -1:
                    groundtruth_file = value

            filepath: str = os.path.join(self._directory, filename)
            groundtruth_path: str = os.path.join(self._directory, groundtruth_file)

            processed_image = Image.open(filepath)
            groundtruth = Image.open(groundtruth_path)
            results: Results = self._compare_images(groundtruth, processed_image)
            self._store_results(algo, dataset, results)

    def _compare_images(self, ground_truth, processed_image) -> Results:

        '''Comparing 2 images and returning the results'''

        if not (ground_truth.size == processed_image.size):
            print("Please provide 2 images with same size")
            return {
                "tn": 0,
                "tp": 0,
                "fn": 0,
                "fp": 0,
                "accuracy": 0
            }

        if not (ground_truth.mode == "L"):
            ground_truth = ground_truth.convert(mode="L")

        if not (processed_image.mode == "L"):
            processed_image = processed_image.convert(mode="L")

        ground_truth_list: list[int] = list(ground_truth.getdata())
        processed_image_list: list[int] = list(processed_image.getdata())

        tn: int = 0
        tp: int = 0
        fn: int = 0
        fp: int = 0

        for i in range(len(ground_truth_list)):
            if ground_truth_list[i] < 128 and processed_image_list[i] < 128:
                # True Negative
                tn += 1
            elif ground_truth_list[i] >= 128 and processed_image_list[i] >= 128:
                # True Positive
                tp += 1
            elif ground_truth_list[i] >= 128 and processed_image_list[i] < 128:
                # False Negative
                fn += 1
            elif ground_truth_list[i] < 128 and processed_image_list[i] >= 128:
                # False Positive
                fp += 1

        return {
            "tn": tn,
            "tp": tp,
            "fn": fn,
            "fp": fp,
            "accuracy": (tn + tp) / (tn + tp + fn + fp)
        }
    
    def _store_results(self, algo: str, dataset: str, results: Results):

        '''Storing the comparison results in the different lists'''
        
        self._images_results.append({
                "algo": algo,
                "dataset": dataset,
                "results": results
            })
        
        self._algos_results[algo].append(results)
        self._datasets_results[dataset].append(results)

    def _compute_algos_stats(self):

        '''Computing average accuracy for each algo'''

        for algo in ALGORITHMS:
            accuracies: list[float] = []

            for result in self._algos_results[algo]:
                accuracies.append(result['accuracy'])
            
            self._algos_stats.append({"algo": algo, "accuracy": statistics.fmean(accuracies)})

    def _compute_datasets_stats(self):

        '''Computing average accuracy for each dataset'''

        for dataset in DATASETS:
            accuracies: list[float] = []

            for result in self._datasets_results[dataset]:
                accuracies.append(result['accuracy'])
            
            self._datasets_stats.append({"dataset": dataset, "accuracy": statistics.fmean(accuracies)})
    
    def _create_benchmarks_directory(self):

        '''Creating directory to store the results if not present'''

        PATH: str = 'benchmarks'

        if not os.path.exists(PATH):
            os.makedirs(PATH)
    
    def get_images_results(self) -> list[ImageResults]:
        return self._images_results

    def print_images_results(self):

        '''Printing all computed comparisons'''

        for result in self._images_results:
            print(result)
    
    def print_algos_results(self):

        '''Printing average accuracies of algos'''

        print('ALGO RESULTS')
        print('------------')

        for algo, results in self._algos_results.items():
            print(f'{algo} : {results}')
    
    def print_dataset_results(self):

        '''Printing average accuracies of datasets'''

        print('DATASET RESULTS')
        print('------------')
        
        for dataset, results in self._datasets_results.items():
            print(f'{dataset} : {results}')
    
    def print_global_accuracy(self):

        '''Printing the average accuracy of all computed comparisons'''

        accuracies: list[float] = []

        for result in self._images_results:
            accuracies.append(result["results"]["accuracy"])
        
        print(statistics.fmean(accuracies))
    
    def export_images_results(self):

        '''Exporting all computed comparisons in a file'''

        self._create_benchmarks_directory()
        with open(r'benchmarks\images_results.txt', 'w') as file:

            for result in self._images_results:
                line: str = f'Algo : {result["algo"]} - '
                line = line + f'Dataset : {result["dataset"]} - '
                line = line + f'TN : {result["results"]["tn"]}, '
                line = line + f'TP : {result["results"]["tp"]}, '
                line = line + f'FN : {result["results"]["fn"]}, '
                line = line + f'FP : {result["results"]["fp"]}, '
                line = line + f'accuracy : {result["results"]["accuracy"]}'
                file.write(line)
                file.write('\n')

            file.close()

    def export_algos_stats(self):

        '''Exporting average accuracies of algos in a file'''

        self._create_benchmarks_directory()
        with open(r'benchmarks\algos_stats.txt', 'w') as file:
            
            for result in self._algos_stats:
                line: str = f'Algo : {result["algo"]} - '
                line = line + f'Accuracy : {result["accuracy"]}'
                file.write(line)
                file.write('\n')

            file.close()

    def export_datatsets_stats(self):

        '''Exporting average accuracies of datasets in a file'''

        self._create_benchmarks_directory()
        with open(r'benchmarks\datatsets_stats.txt', 'w') as file:

            for result in self._datasets_stats:
                line: str = f'Dataset : {result["dataset"]} - '
                line = line + f'Accuracy : {result["accuracy"]}'
                file.write(line)
                file.write('\n')

            file.close()
    