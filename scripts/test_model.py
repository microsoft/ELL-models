#!/usr/bin/env python3
####################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     test_model.py
##  Authors:  Lisa Ong
##
##  Requires: Python 3.x
##
####################################################################################################

import os
import sys
import argparse
from os.path import basename, isdir, join, splitext

if not 'ell_root' in os.environ:
    raise EnvironmentError("ell_root environment variable not set")
_ell_root = os.environ['ell_root']
sys.path.append(join(_ell_root, 'tools/utilities/pitest'))
sys.path.append(join(_ell_root, 'tools/utilities/pythonlibs'))
sys.path.append(join(_ell_root, 'tools/utilities/pythonlibs/gallery'))
import logger

_current_script = os.path.basename(__file__)

class TestModel:
    def __init__(self, path=None, labels=None, target=None, cluster=None,
        val_set=None, val_map=None, test_dir=None):

        self.path = path
        self.labels = labels
        self.target = target
        self.cluster_address = cluster
        self.val_set = val_set
        self.val_map = val_map
        self.test_dir = test_dir

        self.logger = logger.get()
        self.model = None
        self.model_name = None
        self.cluster = None
        self.machine = None

        if not self.path:
            self.path = os.getcwd()
        elif not isdir(self.path):
            raise NotADirectoryError("{} is not a folder".format(self.path))

        for f in os.listdir(self.path):
            if f.endswith(".ell.zip"):
                self.model = join(self.path, f)
                self.model_name = splitext(splitext(basename(f))[0])[0]
                break

        self._get_machine(self.cluster_address)
        self.model_deploy_dir = "/home/pi/test"
        self.validation_deploy_dir = "/home/pi/validation"

    def _cleanup(self):
        "Unlocks the target device if it is part of a cluster"
        if self.machine:
            f = self.cluster.unlock(self.machine.ip_address)
            if f.current_user_name:
                self.logger.error("Failed to free the machine at " + self.machine.ip_address)
            else:
                self.logger.info("Freed machine at " + self.machine.ip_address)

    def __enter__(self):
        """Called when this object is instantiated with 'with'"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called on cleanup of this object that was instantiated with 'with'"""
        self._cleanup()

    def _get_machine(self, cluster):
        "Acquires a machine ipaddress from the cluster"
        picluster = __import__("picluster")

        task = " ".join((_current_script, self.path))
        self.cluster = picluster.PiBoardTable(cluster)
        self.machine = self.cluster.wait_for_free_machine(task)
        self.logger.info("Locked machine at " + self.machine.ip_address)

    def _deploy_model(self):
        "Deploys the model to the target device"
        drivetest = __import__("drivetest")
        with drivetest.DriveTest(ipaddress = self.machine.ip_address,
                target=self.target, labels=self.labels, 
                model=self.model, target_dir=self.model_deploy_dir,
                outdir=self.test_dir,
                profile=True  # emit profiler for raw C++ numbers
                # Note: we don't provide --cluster because we've already locked the machine
            ) as driver:
            driver.run_test()

    def _deploy_validation_set(self):
        "Deploys the validation set to the target device"
        copy_validation_set = __import__("copy_validation_set")
        with copy_validation_set.CopyValidationSet() as cvs:
            cvs.parse_command_line([
                self.val_map,
                self.val_set,
                self.machine.ip_address,
                "--maxfiles", "10",
                "--target_dir", self.validation_deploy_dir
                # Note: we don't provide --cluster because we've already locked the machine
            ])
            cvs.run()

    def _run_test(self):
        "Tests the model on the target device"
        run_validation = __import__("run_validation")
        with run_validation.RunValidation() as rv:
            rv.parse_command_line([
                self.model_name,
                self.machine.ip_address,
                "--maxfiles", "10",
                "--labels", self.labels,
                "--truth", "/home/pi/validation/val_map.txt",
                "--images", "/home/pi/validation",
                "--target", self.target,
                "--target_dir", self.model_deploy_dir,
                "--test_dir", self.test_dir
                # Note: we don't provide --cluster because we've already locked the machine
            ])
            rv.run()

        # collect results
        def rename_output(outfile):
            from shutil import move
            split = splitext(basename(outfile))
            move(join(os.curdir, self.test_dir, self.target, self.model_name, outfile),
                join(self.path, "{}_{}{}".format(split[0], self.target, split[1])))

        rename_output("validation.json")
        rename_output("validation.out")
        rename_output("procmon.json")

    def _generate_markdown(self):
        "Generates a markdown file for the model using the model metadata and test results"
        generate_md = __import__("generate_md")
        gm = generate_md.GenerateMarkdown()
        gm.parse_command_line([
            self.path,
            join(_ell_root, "docs/gallery/ILSVRC2012/{}.md".format(self.model_name)),
            join(_ell_root, "build/bin/Release/print.exe")
        ])
        gm.run()

    def run(self):
        """Main run method"""
        self._deploy_model()
        self._deploy_validation_set()
        self._run_test()
        self._generate_markdown()

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser("This script tests a given ELL model on a target machine\n")

    arg_parser.add_argument("--path", help="the model folder path (or current directory if not specified)", default=None)
    arg_parser.add_argument("--labels", help="path to the labels file for evaluating the model", default="categories.txt")
    arg_parser.add_argument("--target", help="the target platform", choices=["pi0", "pi3"], default="pi3")
    arg_parser.add_argument("--cluster", help="http address of the cluster server that controls access to the target devices",
                            default=None, required=True)
    arg_parser.add_argument("--val_set", help="path to the validation set images", required=True)
    arg_parser.add_argument("--val_map", help="path to the validation set truth", required=True)
    arg_parser.add_argument("--test_dir", help="the folder on the host to collect model files", default="test")

    args = arg_parser.parse_args()

    with TestModel(args.path, args.labels, args.target, args.cluster, args.val_set, args.val_map, args.test_dir) as program:
        program.run()
