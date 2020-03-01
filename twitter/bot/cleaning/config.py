

import os
print(os.getcwd())
corpus_name = "cornell movie-dialogs corpus"
corpus = os.path.join("bot\\data", corpus_name)
movie_lines = os.path.join(corpus, "movie_lines.txt")
movie_conversation = os.path.join(corpus, "movie_conversations.txt")
datafile = os.path.join(corpus, "formatted_movie_lines.txt")
save_dir = os.path.join("bot\\data", "save")