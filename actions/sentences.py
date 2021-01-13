from inltk.inltk import get_similar_sentences

#get_similar_sentences(sentence, no_of_variants,'<code-of-language>', degree_of_aug=0.1)

# where degree_of_aug is roughly the percentage of sentence you want to augment, with a default value of 0.1

print(get_similar_sentences("કપાસ માં ફૂગ સમસ્યા",10,"gu"))
