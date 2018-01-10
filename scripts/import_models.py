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
from os.path import basename, isdir, isfile, join, splitext

def find_model_paths(path, zipped=False):
    "Finds model directories under the given path."

    ext = ".cntk"
    if zipped:
        ext += ".zip"

    # search for model.cntk or model.cntk.zip
    result = [join(path, model, model + ext) for model in os.listdir(path) \
        if isfile(join(path, model, model + ext))]

    return result

class ImportModels:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            "This script imports CNTK models to ELL from a given search path\n")

        self.path = None

        if not 'ell_root' in os.environ:
            raise EnvironmentError("ell_root environment variable not set")
        self.ell_root = os.environ['ell_root']

    def parse_command_line(self, argv): 
        """Parses command line arguments"""
        self.arg_parser.add_argument("--path", help="the search path", default=None)

        args = self.arg_parser.parse_args(argv)
        self.path = args.path

        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))

    def run(self):
        """Main run method"""
        sys.path.append(join(self.ell_root, 'tools/utilities/pythonlibs'))
        ziptools = __import__("ziptools")
        zipper = ziptools.Zipper()

        # Extract zipped CNTK models if the uncompressed versions don't exist
        # (reasoning: .cntk may be more recent than the .cntk.zip)
        zipped_paths = find_model_paths(self.path, zipped=True)
        for zipped in zipped_paths:
            unzipped = splitext(basename(zipped))[0]
            if not isfile(join(self.path, unzipped)):
                print("Extracting: " + zipped)
                unzip = ziptools.Extractor(zipped)
                unzip.extract_file(".cntk")

        # Import uncompressed CNTK models
        sys.path.append(join(self.ell_root, 'tools/importers/CNTK'))
        importer = __import__("cntk_import")

        model_paths = find_model_paths(self.path, zipped=False)
        for model in model_paths:
            print("Importing: " + model)
            importer.main([model, "--zip_ell_model"])

            # Zip up the CNTK model
            # (reasoning: .cntk may be more recent than the .cntk.zip)
            print("Compressing: " + model)
            zipper.zip_file(model, model + ".zip")

if __name__ == "__main__":
    program = ImportModels()
    program.parse_command_line(sys.argv[1:]) # drop the first argument (program name)
    program.run()