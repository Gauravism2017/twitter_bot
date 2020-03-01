import unicodedata
import re
from bot.trimming.VOC import Voc
MAX_LENGTH = 20

f = open('file.txt', 'w', encoding="utf-8")

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'MN'
        )

def normalizeString(s):
    #print(s)
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    #print(s)
    return s

def readVocs(datafile, corpus_name):
    print("Reading lines")
    lines = open(datafile, encoding="utf-8").read().strip().split('\n')
    lines = [line for line in lines if line != '']
    #print(lines, file=f)
    pairs = [[normalizeString(s) for s in l.split('\t')] for l in lines]
    voc = Voc(corpus_name)
    return voc, pairs

def filterPair(p):
    return len(p[0].split(' ')) < MAX_LENGTH and len(p[1].split(' ')) < MAX_LENGHTH

def filterPairs(pairs):
    return [pair for pair in pairs if filterPair(pair)]

def loadPrepareData(corpus, corpus_name, datafile, save_dir):
    print("Start Preparing training data...")
    voc, pairs = readVocs(datafile, corpus_name)
    print("Read {!s} sentence pairs".format(len(pairs)))
    print("Counted words:")
    #print(pairs, file=f)
    for pair in pairs:
        #print(pair)
        voc.addSentence(pair[0])
        voc.addSentence(pair[1])
        #if len(pair) == 2:
        #    #print(pair)
        #    voc.addSentence(pair[0])
        #    voc.addSentence(pair[1])
    print("Counted Words :", voc.num_words)
    return voc, pairs



