#!/usr/bin/env python3
####################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     import_models.py
##  Authors:  Lisa Ong
##
##  Requires: Python 3.x
##
####################################################################################################
import os
import sys
import argparse
import glob
from os.path import basename, isdir, isfile, join, splitext

if not 'ell_root' in os.environ:
    raise EnvironmentError("ell_root environment variable not set")
_ell_root = os.environ['ell_root']
sys.path.append(join(_ell_root, 'tools/utilities/pythonlibs'))
sys.path.append(join(_ell_root, 'tools/importers/CNTK'))
import cntk_import as importer
import logger
import ziptools

def find_model_paths(path, zipped=False):
    "Finds model directories under the given path."

    ext = "cntk"
    if zipped:
        ext += ".zip"

    # Exclude _arch.cntk, _final.cntk, _indexN+_errorN+.cntk
    result = sorted(list(set(glob.glob("{}/**/*.{}".format(path, ext), recursive=True)) -
             set(glob.glob("{}/**/*_arch.{}".format(path, ext), recursive=True)) -
             set(glob.glob("{}/**/*_final.{}".format(path, ext), recursive=True)) -
             set(glob.glob("{}/**/*_index*_error*.{}".format(path, ext), recursive=True))))

    return result

class ImportModels:
    def __init__(self, path=None, logfile=None):
        self.path = path
        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))
        self.logger = logger.get(logfile)
        self.logger.info(sys.argv)

    def run(self):
        """Main run method"""
        # Extract zipped CNTK models if the uncompressed versions don't exist
        # (reasoning: .cntk may be more recent than the .cntk.zip)
        zipped_paths = find_model_paths(self.path, zipped=True)
        for zipped in zipped_paths:
            unzipped = splitext(basename(zipped))[0]
            if not isfile(join(self.path, unzipped)):
                self.logger.info("Extracting: " + zipped)
                unzip = ziptools.Extractor(zipped)
                unzip.extract_file(".cntk")

        # Import uncompressed CNTK models
        model_paths = find_model_paths(self.path, zipped=False)
        zipper = ziptools.Zipper()
        for model in model_paths:
            self.logger.info("Importing: " + model)
            importer.main([model, "--zip_ell_model"])

            # Zip up the CNTK model
            # (reasoning: .cntk may be more recent than the .cntk.zip)
            self.logger.info("Compressing: " + model)
            zipper.zip_file(model, model + ".zip")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        "This script imports CNTK models to ELL from a given search path\n")
    arg_parser.add_argument("--path", help="the search path", default=None)
    arg_parser.add_argument("--logfile", help="path to a log file (in addition to console logging)", default=None)

    args = arg_parser.parse_args()
    program = ImportModels(args.path, args.logfile)
    program.run()