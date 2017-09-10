# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys
from bosonnlp import BosonNLP
#api='MCLqty62.15052.G-lgogParh9C';
api='eF4xmB2b.15587.-X89nqAWr7qj'
#api='bpbdHnxG.15205.vMueDo_dTgh7'
nlp = BosonNLP(api);



#专有词汇
def specialword(sentence):
    result=nlp.ner(sentence, sensitivity=2);
    result=result[0];
    return result;
def getTimewords(result):
    entities_word=result['word'];
    entities=result['entity'];
    specialnounlist=[];
    if(len(entities)>0):
        for entity in entities:
            #处理专有词汇
            if(entity[2]=='time'):
                sumofwords=entity[1]-entity[0];
                while(sumofwords>=1):
                    specialnounlist.append(entities_word[sumofwords+entity[0]-1]);
                    sumofwords=sumofwords-1;
        return specialnounlist;


#分词
def participle(sentence):
    result=nlp.tag(sentence);
    result=result[0];
    return result;
def participle_word(result):
    wordlist=result['word'];
    return wordlist;
def participle_cixing(result):
    cixinglist=result['tag'];
    return cixinglist;
def getDaiciIndex(result):
    cixinglist=result['tag'];
    #找最远代词
    if 'r' in cixinglist:
        index=cixinglist.index('r');
        real_index=index;
        if(index!=-1):
            index=index+1;
            while(index<len(cixinglist)):
                if(cixinglist[index]=='r'):
                    real_index=index;
                index=index+1;
        return real_index;
    elif 'd' in cixinglist:
        return cixinglist.index('d');
    else:
        return len(cixinglist)-2;

#list类型
def getVerbIndex(result):
    cixinglist=result['tag'];
    VerbList=[i for i,a in enumerate(cixinglist) if a.startswith('v')];
    return VerbList;
#list类型
def getNounIndex(result):
    cixinglist=result['tag'];
    NounList=[i for i,a in enumerate(cixinglist) if a=='n' ];
    return NounList;
#得到助词
def getZhuciIndex(result):
    cixinglist=result['tag'];
    worldlist=result['word']
    ZhuciList=[i for i,a in enumerate(cixinglist) if a=='u' and worldlist[i]=='的'];
    return ZhuciList;



#评分
#match是关键词 search是文本
def getScore(match_word,search_word,keyscore,search_tag,match_tag):
    scoreinit=keyscore/len(match_word);
    score=0;
    length=0;


    while(len(match_word)>length and len(search_word)>length):
        #单字匹配模式，默认为相等，赋予全分
        if(match_word.find(search_word[length])!=-1 and len(search_word)==1 and search_tag==match_tag):
            if(len(match_word)<=3):
                score=score+scoreinit;
            else:
                score=score+scoreinit*len(match_word)/2.0;
        #
        elif(match_word[0]==search_word[0] and len(match_word)!=len(search_word)or (match_word.find(search_word[length])!=-1 and search_tag!=match_tag)):
            score=0;
            break;
        #1.首字母不同且长度不同
        #2.首字母相同且长度相同
        #3.首字母不同且长度相同

        #长度相同情况：
        elif(len(match_word)==len(search_word)):
            if(match_word[length]==search_word[length] ):
                 #同等
                score=score+scoreinit;
            elif(match_word.find(search_word[length])!=-1):
                  #包含
                if(len(search_word)<3):
                    score=score+scoreinit/1.5;

        #长度不相等:
        elif(match_word.find(search_word[length])!=-1):
            #同等
            if(match_word[length]==search_word[length] ):
                score=score+scoreinit/2;
            #包含
            elif(match_word.find(search_word[length])!=-1):
                #如果词过长，那么就算它拥有某一个字基本上没有什么用了
                if(len(search_word)<3):
                    score=score+scoreinit/3;
        # elif(match_word.find(search_word[length])!=-1):
        # score=score+scoreinit/2;
        else:
            score=0;
            break;
        length=length+1;
    return score;





