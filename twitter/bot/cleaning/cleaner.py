import os
#from bot import cleaning
#from bot.cleaning import lookup
import codecs
import csv
from bot.cleaning.config import corpus, movie_lines, movie_conversation, datafile
from bot.cleaning.clean import loadLines, loadConversations, extractSentencePairs
from bot.cleaning.lookup import printLines

delimiter = '\t'

delimiter = str(codecs.decode(delimiter, "unicode_escape"))

lines = {}
conversations = []

MOVIE_LINES_FIELDS = ["lineID", "characterID", "movieID", "character", "text"]
MOVIE_CONVERSATIONS_FIELDS = ["character1ID", "character2ID", "movieID", "utteranceIDs"]

print("\n Processing Corpus")
lines = loadLines(movie_lines, MOVIE_LINES_FIELDS)
print("\nProcessing conversation")
conversations = loadConversations(movie_conversation, lines, 
                                  MOVIE_CONVERSATIONS_FIELDS)
print("\nWriting in new file")
with open(datafile, 'w', encoding="utf-8") as outputfile:
    writer = csv.writer(outputfile, delimiter = delimiter, lineterminator = "\n")
    for pair in extractSentencePairs(conversations):
        writer.writerow(pair)

print("\Sample Lines from new file:")
printLines(datafile)



