import torch
from torch.jit import script, trace
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from bot.model.config import *
from bot.trimming.preprocessing import normalizeString
from bot.trimming.prepare_data import indexesFromSentence
from bot.cleaning.config import save_dir
import re
inp = open(save_dir+"/inp.txt", 'r', encoding="utf-8")
out = open(save_dir+"/out.txt", 'w', encoding="utf-8")

content = inp.readlines()

content = [x.strip() for x in content] 




def evaluate(encoder, decoder, searcher, voc, sentence, max_length=MAX_LENGTH):
    ### Format input sentence as a batch
    # words -> indexes
    indexes_batch = [indexesFromSentence(voc, sentence)]
    # Create lengths tensor
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # Transpose dimensions of batch to match models' expectations
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    # Use appropriate device
    input_batch = input_batch.to(device)
    lengths = lengths.to(device)
    # Decode sentence with searcher
    tokens, scores = searcher(input_batch, lengths, max_length)
    # indexes -> words
    decoded_words = [voc.index2word[token.item()] for token in tokens]
    return decoded_words


#def evaluateInput(encoder, decoder, searcher, voc):
#    #input_sentence = ''
#    for input_sentence in content:
#        try:
#            # Get input sentence
        
#        #input_sentence = input('> ')
#        # Check if it is quit case
#            if input_sentence == 'q' or input_sentence == 'quit': break
#            # Normalize sentence
#            input_sentence = normalizeString(input_sentence)
#            # Evaluate sentence
#            output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
#            # Format and print response sentence
#            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
#            print(' '.join(output_words), file = out)

#        except KeyError:
#            print("Error: Encountered unknown word.")


def evaluateInput(encoder, decoder, searcher, voc):
    #input_sentence = ''
    for input_sentence in content:
        #try:
            # Get input sentence
        
        #input_sentence = input('> ')
        # Check if it is quit case
        if input_sentence == 'q' or input_sentence == 'quit': break
        # Normalize sentence
        input_sentence = normalizeString(input_sentence)
        # Evaluate sentence
        output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
        # Format and print response sentence
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
        print(' '.join(output_words), file = out)

        #except KeyError:
        #    print("Error: Encountered unknown word.")



