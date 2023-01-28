from turkishnlp import detector

obj = detector.TurkishNLP()

fp = open('/home/zeroday/Desktop/cse654_nlp/hw1/archive/temp.txt','r',encoding = 'utf8')
fp2 = open('syllables.txt','w',encoding = 'utf8')

line = fp.read()
arr = obj.syllabicate_sentence(line)

for element in arr:
    for innerelement in element:
        fp2.write(innerelement)
        fp2.write(" ")

fp2.close()
fp.close()