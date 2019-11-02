"""annoying boilerplate to get face.evoLVe working
in the context of a Flask app"""

import os, sys
sys.path.append(os.path.join(os.getcwd(), "face.evoLVe.PyTorch", "align"))
import detector
import contextlib

@contextlib.contextmanager
def peek(dir_path):
    cdir = os.getcwd()
    os.chdir(dir_path)
    yield
    os.chdir(cdir)

def detect_faces(*args, **kwargs):
    """wrapper for detector.detect_faces"""
    with peek("./face.evoLVe.PyTorch/align"):
        return detector.detect_faces(*args, **kwargs)