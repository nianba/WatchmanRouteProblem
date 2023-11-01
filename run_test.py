from wrpsolver.Test.test import RunTest
import sys
if __name__ =='__main__':
    if len(sys.argv) == 2:
        seed = sys.argv[1]
    else:
        seed = 2
    RunTest(int(seed))