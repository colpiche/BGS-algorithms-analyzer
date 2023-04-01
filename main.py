from algo_tester.comparator import Comparator

DIRECTORY: str = "outputs"


def main():
    comparator: Comparator = Comparator(DIRECTORY)
    comparator.start()
    comparator.export_images_results()
    comparator.export_algos_stats()
    comparator.export_datatsets_stats()


if __name__ == "__main__":
    main()
