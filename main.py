import diffpy
import sys

if __name__ == "__main__":

    bb = diffpy.DiffPy('test.txt', 'test2.txt')
    bb.diff()

def start(old, new):
    bb = diffpy.DiffPy(old, new)
    print("heellooo!!!")


    
    