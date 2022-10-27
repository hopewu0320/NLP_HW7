#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
from collections import Counter
from pprint import pprint
import random
#from functools import filter
'''
splits:[('', 'inconvicent'), ('i', 'nconvicent'), ('in', 'convicent'), ('inc', 'onvicent'), ('inco', 'nvicent'), ('incon', 'vicent'), ('inconv', 'icent'), ('inconvi', 'cent'), ('inconvic', 'ent'), ('inconvice', 'nt'), ('inconvicen', 't'), ('inconvicent', '')]
deletes:['orrectud', 'krrectud', 'korectud', 'korectud', 'korrctud', 'korretud', 'korrecud', 'korrectd', 'korrectu']
'''
def words(text): return re.findall(r'\w+', text.lower()) #findall找所有匹配文字

word_count = Counter(words(open('big.txt').read())) #Counter回傳一個dictionary 計算各個詞的出現次數 'the':79809

N = sum(word_count.values())     #dict.values()回傳所有value
def P(word):
    return word_count[word] / N  #回傳frequncy 

#Run the function:

print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'
vowel='aeiou'
example=['dd','ss']



def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    
    deletes    = [L + R[1:]               for L, R in splits if R]  #去除一個letter
    
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]   #交換鄰近位置  
    replaces   = [L + c + R[1:]           for L, R in splits if (len(R)>1 and R[0] in vowel) for c in vowel] #新增!! #改變其中個字母成其他字母 
    
    
    inserts    = [L + c + R               for L, R in splits for c in letters]      #加入一個字母
   
    return set(deletes + transposes + replaces + inserts )   

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits3(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    replaces   = [L + c + R[1:]           for L, R in splits if (len(R)>1 and R[0] in vowel) for c in vowel]
    
    close_cosonants=[L + 's' + R[1:]           for L, R in splits if (len(R)>1 and R[0]=='c') ]
    double_consants=[L + R[0] + R[0] + R[1:]           for L, R in splits if (len(R)>1 and R[0] not in vowel) ]
    
    inserts    = [L + c + c + R               for L, R in splits if (len(R)>1 and R[0] in vowel) for c in vowel]      #加入一個字母
    
    
    return set( replaces + inserts+ close_cosonants + double_consants)

#Run the function:
#pprint( list(edits1('speling'))[:3])
#pprint( list(map(lambda x: (x, P(x)), edits1('speling'))) )    
#pprint( list(filter(lambda x: P(x) != 0.0, edits1('speling'))) )
#pprint( max(edits1('speling'), key=P) )

def correction(word):                   #找出機率(次數)最大的候選人
    return max(candidates(word), key=P,default=0) #輸入candidate('somthing') 回傳:{'something','soothing'}


def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or known(edits3(word))  or [word])
    
    
   
def known(words):           #錯誤的詞語(speling) 在詞典裡
    return set(w for w in words if w in word_count)


print('speling -->', correction('speling'))
# speling spelling

#print('word_count len:{}'.format(len(word_count)))
#print('word_count value:{}'.format(sum(word_count.values())))


def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.perf_counter()
    good, unknown = 0, 0
    n = len(tests)          #n=270
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in word_count)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, word_count[w], right, word_count[right]))
    dt = time.perf_counter() - start
    print('duration time:{:.3f}'.format(dt))
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
    
def Testset(lines):  #return (right,wrong) pairs
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines) #in:['contented', ' contenpted contende contended contentid\n']
            for wrong in wrongs.split()]
#[('contented', ' contenpted contende contended contentid\n'),......] :一二個for的結果


#print(unit_tests())
spelltest(Testset(open('spell-testset1.txt'))) # Development set
spelltest(Testset(open('spell-testset2.txt'))) # Final test set


print('adres->', correction('concider'))
print('adres->', correction('totally'))

def randomly_choose(lines):
    random_list=[]
    word_list= [(right, wrong)
                for (right, wrongs) in (line.split(':') for line in lines) #in:['contented', ' contenpted contende contended contentid\n']
                for wrong in wrongs.split()]
                
    for i in range(100):
        idx=random.randint(0,1)
        random_list.append(word_list[i][idx])
    return random_list