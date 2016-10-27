import pickle, os, sys
basePath = os.path.dirname(__file__)
lines = os.path.join(basePath, "lines.wlia")

data = pickle.load( open( lines, "rb" ) )

print(data)
input()