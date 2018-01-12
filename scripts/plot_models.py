#!/usr/bin/env python3
####################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     plot_models.py
##  Authors:  Lisa Ong
##
##  Requires: Python 3.x
##
####################################################################################################

import os
import sys
import argparse

from os.path import join, isdir

class PlotModels:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            "This script plots all ELL models found under a path.\n")

        self.path = None

        if not 'ell_root' in os.environ:
            raise EnvironmentError("ell_root environment variable not set")
        self.ell_root = os.environ['ell_root']
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
        self._plot_pareto()

if __name__ == "__main__":
    program = PlotModels()
    program.parse_command_line(sys.argv[1:])
    program.run()