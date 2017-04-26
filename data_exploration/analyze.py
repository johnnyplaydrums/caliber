from classify import *
from raw_integration import *
import sys
import datetime

argv = sys.argv[1]
now = datetime.datetime.now()
print(classify(integrate(argv)))
then = datetime.datetime.now()
print(then-now)
classify_graph(integrate(argv))
