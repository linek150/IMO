import sys
import pathlib as path
sys.path.append(str(path.Path(__file__).parents[0]))

from .ExtendedLocalSearch.TestBench import run_test
print("Maint starts...")
run_test()
