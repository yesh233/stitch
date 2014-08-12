import cPickle
import gzip

def save(data, path):
    with gzip.open(path, 'w') as fp:
	cPickle.dump(data, fp)

def load(path):
    with gzip.open(path) as fp:
	return cPickle.load(fp)


