####################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     test_models.py
##  Authors:  Lisa Ong
##
##  Requires: Python 3.x
##
####################################################################################################

import os
import sys
import argparse
import glob
import test_model
from os.path import dirname, isdir, join

def find_model_paths(path):
    "Finds model directories under the given path."

    cwd = os.getcwd()
    os.chdir(path)

    result = glob.glob("**/*.{}".format("ell.zip"), recursive=True)
    os.chdir(cwd)

    return result

class TestModels:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            "This script tests all ELL models found under a path, sequentially.\n"
            "This will be enhanced in the future to run tests in parallel\n"
            "(once drivetest supports multiple instances).\n")

        self.path = None
        self.model_dirs = None

        if not 'ell_root' in os.environ:
            raise EnvironmentError("ell_root environment variable not set")
        self.ell_root = os.environ['ell_root']
        sys.path.append(join(self.ell_root, 'tools/utilities/pitest'))
        sys.path.append(join(self.ell_root, 'tools/utilities/pythonlibs'))
        sys.path.append(join(self.ell_root, 'tools/utilities/pythonlibs/gallery'))

    def parse_command_line(self, argv):
        """Parses command line arguments"""
        self.arg_parser.add_argument("--path", help="the model search path (or current directory if not specified)", default=None)

        args = self.arg_parser.parse_args(argv)
        self.path = args.path

        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))

        self.model_dirs = [dirname(p) for p in find_model_paths(self.path)]

    def _run_tests(self):
        "Tests each model"
        for model_path in self.model_dirs:
            with test_model.TestModel() as tm:
                tm.parse_command_line([
                    "--path", model_path
                ])
                tm.run()

    def _plot_pareto(self):
        "Generates a pareto plot of the models"
        plot_model_stats = __import__("plot_model_stats")
        plotter = plot_model_stats.PlotModelStats()
        plotter.parse_command_line([
            self.path,
            "--output_figure", "speed_v_accuracy_pi3.png"
        ])
        plotter.run()

    def run(self):
        "Main run method"
        self._run_tests()
        self._plot_pareto()

if __name__ == "__main__":
    program = TestModels()
    program.parse_command_line(sys.argv[1:])
    program.run()