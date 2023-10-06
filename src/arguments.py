import argparse
import sys

class Arguments:
    def __init__(self):
        self.sorting = None
        self.all_media = False

    @staticmethod
    def get_args():
        return Arguments.instance

    @staticmethod
    def read_args():
        if hasattr(Arguments, "instance"):
            return

        parser = argparse.ArgumentParser(description="Your program description")
        parser.add_argument("-s", "--sort", help="Sorting option", choices=["option1", "option2"])
        parser.add_argument("-C", "--all-media", help="All media", action="store_true")

        args = parser.parse_args()

        Arguments.instance = Arguments()
        Arguments.instance.sorting = args.sort
        Arguments.instance.all_media = args.all_media

# Initialize arguments
Arguments.read_args()
