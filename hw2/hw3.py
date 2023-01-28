from nltk import ngrams
from gensim.models import Word2Vec

fp = open('syllables.txt','r',encoding = 'utf8')

syllables = fp.read()
uni_grams = ngrams(syllables.split(), 1)
bi_grams = ngrams(syllables.split(), 2)
tri_grams = ngrams(syllables.split(), 3)  

uni_arr = list(uni_grams)
bi_arr = list(bi_grams)
tri_arr = list(tri_grams)


result = [x[0] for x in uni_arr]
result += [' '.join(x) for x in bi_arr]
result += [' '.join(x) for x in tri_arr]

my_model = Word2Vec([result], min_count=1, vector_size=100, window=5)

# word embeddings
print("############### syllable vectors for uni gram###############")
print("'fil'\n", my_model.wv['fil'])
print("'min'\n", my_model.wv['min'])
print("'mü'\n", my_model.wv['mü'])
print("'zik'\n", my_model.wv['zik'])
print("'le'\n", my_model.wv['le'])
print("'ri'\n", my_model.wv['ri'])
print("'ni'\n", my_model.wv['ni'])

print("\n\n")

print("############### syllable vectors for bi gram############### ")
print("'e lekt'\n", my_model.wv['e lekt'])
print("'ge len'\n", my_model.wv['ge len'])
print("'nen ce'\n", my_model.wv['nen ce'])
print("'al dı'\n", my_model.wv['al dı'])
print("'ge le'\n", my_model.wv['ge le'])
print("'yı lın'\n", my_model.wv['yı lın'])
print("'zal dı'\n", my_model.wv['zal dı'])
print("'ro nik'\n", my_model.wv[ 'ro nik'])

print("\n\n")

print("############### syllable vectors for tri gram############### ")
print("'çek ti la'\n", my_model.wv['çek ti la'])
print("'ti la rın'\n", my_model.wv['ti la rın'])
print("'la rın son'\n", my_model.wv['la rın son'])
print("'rın son la'\n", my_model.wv['rın son la'])
print("'son la rı'\n", my_model.wv['son la rı'])
print("'la rı na'\n", my_model.wv['la rı na'])
print("'rı na doğ'\n", my_model.wv['rı na doğ'])
print("'na doğ ru'\n", my_model.wv[ 'na doğ ru'])

print("\n\n")


#similarities
print("################ similarities for uni-grams ###############\n")
print("'lar', 'ar'", my_model.wv.similarity('lar', 'ar'))
print("'rak', 'sans'", my_model.wv.similarity('rak', 'sans'))

print("\n\n")

print("################ similarities for bi-grams ###############\n")
print("'ge le', 'ge len'", my_model.wv.similarity('ge le', 'ge len'))
print("'ge le', 'nen ce'", my_model.wv.similarity('ge le', 'nen ce'))
print("'e lekt', 'ro nik'", my_model.wv.similarity('e lekt', 'ro nik'))
print("'al dı', 'zal dı'", my_model.wv.similarity('al dı', 'zal dı'))
print("'al dı', 'ro nik'", my_model.wv.similarity('al dı', 'ro nik'))


print("\n\n")

print("################ similarities for tri-grams ###############\n")
print("'o la rak', 'la rak bir'", my_model.wv.similarity('o la rak', 'la rak bir'))
print("'o la rak', 'ün ka zan'", my_model.wv.similarity('o la rak', 'ün ka zan'))

print("\n\n")
print("\n\n")

# most similar
print(my_model.wv.most_similar(positive=['top', 'la'], negative=['dı']))
print("\n")
print(my_model.wv.most_similar(positive=['cen', 'han'], negative=['giz']))
print("\n")
print(my_model.wv.most_similar(positive=['mo', 'lis'], negative=['ğo']))
print("\n")
print(my_model.wv.most_similar(positive=['hu kuk ve', 've ik ti'], negative=['kuk ve ik']))
print("\n")
print(my_model.wv.most_similar(positive=['ya kın', 'liş'], negative=['i']))