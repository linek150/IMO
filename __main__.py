import sys
import pathlib as path
sys.path.append(str(path.Path(__file__).parents[0]))
print("Main starts...")
#place your imports below
from .GeneticSearch.TestBench import run_test


run_test(10,300)




