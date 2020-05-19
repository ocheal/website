import os, sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", action="store_true",
                        help="run server from frozen files")
    parser.add_argument("--build", action="store_true",
                        help="build frozen files without hosting a server")
    args = parser.parse_args()
    if (args.build and args.frozen):
        raise ValueError("Mututally exclusive options build and frozen can't both be set")
    return parser.parse_args()

# If running as local (not installed) module or as script
if (__package__ == "") or (__package__ is None):
    # Add directory above directory of __file__
    # to sys.path, so that website can be imported.
    fspath = os.path.abspath(__file__)
    path = os.path.dirname(os.path.dirname(fspath))
    sys.path.insert(0, path)

from website import app

args = parse_args()
if args.build or args.frozen:
    from .freezer import freezer
    if args.build:
        freezer.freeze()
    else:
        freezer.run(port=5000, debug=True)
else:
    app.run(port=5000, debug=True)
