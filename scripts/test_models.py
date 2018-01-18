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
import test_model

from os.path import basename, dirname, isdir, join, splitext

if not 'ell_root' in os.environ:
    raise EnvironmentError("ell_root environment variable not set")
_ell_root = os.environ['ell_root']
sys.path.append(join(_ell_root, 'tools/utilities/pitest'))
sys.path.append(join(_ell_root, 'tools/utilities/pythonlibs'))
sys.path.append(join(_ell_root, 'tools/utilities/pythonlibs/gallery'))
import logger

def find_model_paths(path):
    "Finds model directories under the given path."
    result = glob.glob("{}/**/*.{}".format(path, "ell.zip"), recursive=True)
    return result

class TestModels:
    def __init__(self, path=None, parallel=True, max_threads=None, labels="categories.txt",
        target="pi3", cluster=None, val_set=None, val_map=None, logfile=None):
        self.path = path
        self.parallel = parallel
        self.max_threads = max_threads
        self.val_map = val_map
        self.val_set = val_set
        self.cluster = cluster
        self.target = target
        self.labels = labels

        self.model_dirs = None

        # in parallel mode, prepend all log messages with the thread id
        # so we can make sense of parallel output
        self.logger = logger.get(filepath=logfile, log_thread_id=self.parallel)

        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))

        self.model_dirs = [dirname(p) for p in find_model_paths(self.path)]

    def _run_test(self, model_path):
        try:
            with test_model.TestModel(model_path, self.labels, self.target,
                self.cluster, self.val_set, self.val_map,
                splitext(basename(model_path))[0] + "_t") as tm:
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
    arg_parser = argparse.ArgumentParser(
        "This script tests all ELL models found under a path, sequentially or in parallel.\n")

    arg_parser.add_argument("--path", help="the model search path (or current directory if not specified)", default=None)
    arg_parser.add_argument("--parallel", type=bool, help="test models in parallel (defaults to True)", default=True)
    arg_parser.add_argument("--max_threads", type=int, help="maximum number of threads to use (defaults to number of cores)", default=None)
    arg_parser.add_argument("--labels", help="path to the labels file for evaluating the model", default="categories.txt")
    arg_parser.add_argument("--target", help="the target platform", choices=["pi0", "pi3"], default="pi3")
    arg_parser.add_argument("--cluster", help="http address of the cluster server that controls access to the target devices", required=True)
    arg_parser.add_argument("--val_set", help="path to the validation set images", required=True)
    arg_parser.add_argument("--val_map", help="path to the validation set truth", required=True)
    arg_parser.add_argument("--logfile", help="path to a log file (in addition to console logging)", default=None)

    args = arg_parser.parse_args()

    program = TestModels(args.path, args.parallel, args.max_threads, args.labels,
        args.target, args.cluster, args.val_set, args.val_map, args.logfile)
    program.run()