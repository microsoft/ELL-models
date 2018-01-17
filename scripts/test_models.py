#!/usr/bin/env python3
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
import logging
import test_model

from os.path import basename, dirname, isdir, join, splitext

def find_model_paths(path):
    "Finds model directories under the given path."
    result = glob.glob("{}/**/*.{}".format(path, "ell.zip"), recursive=True)
    return result

class TestModels:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            "This script tests all ELL models found under a path, sequentially or in parallel.\n")

        self.path = None
        self.model_dirs = None
        self.parallel = True
        self.max_threads = None
        self.val_map = None
        self.val_set = None
        self.cluster = None
        self.target = "pi3"
        self.labels = None
        self.logger = logging.getLogger(__name__)

        if not 'ell_root' in os.environ:
            raise EnvironmentError("ell_root environment variable not set")
        self.ell_root = os.environ['ell_root']
        sys.path.append(join(self.ell_root, 'tools/utilities/pitest'))
        sys.path.append(join(self.ell_root, 'tools/utilities/pythonlibs'))
        sys.path.append(join(self.ell_root, 'tools/utilities/pythonlibs/gallery'))

    def parse_command_line(self, argv):
        """Parses command line arguments"""
        self.arg_parser.add_argument("--path", help="the model search path (or current directory if not specified)", default=None)
        self.arg_parser.add_argument("--parallel", type=bool, help="test models in parallel (defaults to True)", default=True)
        self.arg_parser.add_argument("--max_threads", type=int, help="maximum number of threads to use (defaults to number of cores)", default=None)
        self.arg_parser.add_argument("--labels", help="path to the labels file for evaluating the model", default="categories.txt")
        self.arg_parser.add_argument("--target", help="the target platform", choices=["pi0", "pi3"], default="pi3")
        self.arg_parser.add_argument("--cluster", help="http address of the cluster server that controls access to the target devices", required=True)
        self.arg_parser.add_argument("--val_set", help="path to the validation set images", required=True)
        self.arg_parser.add_argument("--val_map", help="path to the validation set truth", required=True)

        args = self.arg_parser.parse_args(argv)
        self.path = args.path
        self.parallel = args.parallel
        self.max_threads = args.max_threads
        self.labels = args.labels
        self.target = args.target
        self.cluster = args.cluster
        self.val_set = args.val_set
        self.val_map = args.val_map

        if self.parallel:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(thread)d]: %(message)s")
        else:
            logging.basicConfig(level=logging.INFO, format="%(message)s")

        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))

        self.model_dirs = [dirname(p) for p in find_model_paths(self.path)]

    def _run_test(self, model_path):
        try:
            with test_model.TestModel() as tm:
                tm.parse_command_line([
                    "--path", model_path,
                    "--test_dir", splitext(basename(model_path))[0] + "_pitest",
                    "--labels", self.labels,
                    "--target", self.target,
                    "--cluster", self.cluster,
                    "--val_set", self.val_set,
                    "--val_map", self.val_map
                ])
                tm.run()
        except:
            errorType, value, traceback = sys.exc_info()
            self.logger.error("### Exception: " + str(errorType) + ": " + str(value))
            return False
        return True

    def _run_tests(self):
        "Tests each model"
        if self.parallel:
            self.logger.info("Running in parallel")
            import dask.threaded
            from dask import compute, delayed, set_options
            from multiprocessing.pool import ThreadPool

            if self.max_threads:
                self.logger.info("Max threads: %d" % (self.max_threads))

                dask.set_options(pool=ThreadPool(self.max_threads))

            values = [delayed(self._run_test)(model_path) for model_path in self.model_dirs]
            compute(*values, get=dask.threaded.get)
        else:
            self.logger.info("Running sequentially")
            for model_path in self.model_dirs:
                self._run_test(model_path)

    def run(self):
        "Main run method"
        self._run_tests()

if __name__ == "__main__":
    program = TestModels()
    program.parse_command_line(sys.argv[1:])
    program.run()