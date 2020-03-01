
import random
import torch
import os
from torch.jit import script, trace
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from bot.cleaning.config import corpus, movie_lines, movie_conversation, datafile, save_dir, corpus_name
from bot.trimming.preprocessing import loadPrepareData
from bot.trimming.trimwords import trimRareWords
from bot.trimming.prepare_data import batch2TrainData
from bot.model.EncoderRNN import EncoderRNN
from bot.model.LuongAttentionDecoder import LuongAttnDecoderRNN
from bot.model.LuongAttn import Attn
from bot.model.train import trainIters
from bot.model.config import *
from bot.model.evaluate import evaluateInput
from bot.model.GreedySearchDecoder import GreedySearchDecoder
MAX_LENGTH = 20


#USE_CUDA = torch.cuda.is_available()
#device = torch.device("cuda" if USE_CUDA else "cpu")

voc, pairs = loadPrepareData(corpus, corpus_name,
                             datafile, save_dir)
MIN_COUNT = 3
small_batch_size = 5
pairs = trimRareWords(voc, pairs, MIN_COUNT)
batches = batch2TrainData(voc, [random.choice(pairs) for _ in range(small_batch_size)])
input_variable, lengths, target_variable, mask , max_target_len = batches
#print("\npairs")
#for pair in pairs[:10]:
#    print(pair)

#print("input_variable:", input_variable)
#print("lengths:", lengths)
#print("target_variable:", target_variable)
#print("mask:", mask)
#print("max_target_len:", max_target_len)



# Set checkpoint to load from; set to None if starting from scratch
loadFilename = None
checkpoint_iter = 6000
loadFilename = os.path.join(save_dir, model_name, corpus_name,
                            '{}-{}_{}'.format(encoder_n_layers, decoder_n_layers, hidden_size),
                            '{}_checkpoint.tar'.format(checkpoint_iter))


# Load model if a loadFilename is provided
print(loadFilename)

if loadFilename:
    print("Entered")
    # If loading on same machine the model was trained on
    checkpoint = torch.load(loadFilename)
    # If loading a model trained on GPU to CPU
    #checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    embedding_sd = checkpoint['embedding']
    voc.__dict__ = checkpoint['voc_dict']
    print("model loaded")


print('Building encoder and decoder ...')
# Initialize word embeddings
embedding = nn.Embedding(voc.num_words, hidden_size )
if loadFilename:
    embedding.load_state_dict(embedding_sd)
# Initialize encoder & decoder models
encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
if loadFilename:
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)
# Use appropriate device
encoder = encoder.to(device)
decoder = decoder.to(device)
print('Models built and ready to go!')



# Initialize optimizers
print('Building optimizers ...')
encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
if loadFilename:
    encoder_optimizer.load_state_dict(encoder_optimizer_sd)
    decoder_optimizer.load_state_dict(decoder_optimizer_sd)

# If you have cuda, configure cuda to call
for state in encoder_optimizer.state.values():
    for k, v in state.items():
        if isinstance(v, torch.Tensor):
            state[k] = v.cuda()

for state in decoder_optimizer.state.values():
    for k, v in state.items():
        if isinstance(v, torch.Tensor):
            state[k] = v.cuda()

encoder.eval()
decoder.eval()

# Initialize search module
searcher = GreedySearchDecoder(encoder, decoder)

# Begin chatting (uncomment and run the following line to begin)
evaluateInput(encoder, decoder, searcher, voc)
