#-*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import copy


import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import test
import utiltest
import time
f = open("youwenti");
w=open("linescores",'w');
question=''
line=f.readline();
scoredict={};
key_list=[];
#储存分数列表，只取前4个
scoresum={};



while line:
    sentences=line.split();



    if(question!=sentences[0]):
        question=sentences[0];
        scoredict=utiltest.keyDict(question);
        key_list=scoredict.keys();
    key_list_temp=copy.deepcopy(key_list);
    content='';
    contentindex=1;
    while(contentindex<len(sentences)):
        content=content+sentences[contentindex];
        contentindex=contentindex+1;


#测试 content为每一行内容 question为问题
    answer_type=utiltest.problemsort(question);
    answer_key=utiltest.problem_key(question);
    typeflag=1;
    keyflag=1;
    linescore=0;
    for keyword in key_list_temp:
        scoresum[keyword]=0;
    result=test.participle(content);
    Wordlist=test.participle_word(result);
    Taglist=test.participle_cixing(result);

    for word in Wordlist:  #对于文本中文list中的每个分词word
        for keyword in key_list_temp:  #对于问题中文list中的每个分词keyword

            #根据是否符合问题的类型给这一行文本打分
            if(answer_type in Taglist and typeflag==1): #如果文本中的词性list中有问题的类型
                if(type(answer_key)==list and utiltest.doubleadd(answer_key,Wordlist,Taglist,'t')): #若answer_key为list类型，即问题中有多个表示时间的关键字
                     linescore=linescore+0.8*len(key_list);
                     typeflag=0;

            #根据是否含有问题中时间类型的关键字给这一行文本打分
            if(type(answer_key)==list and keyflag==1):
                if(word==answer_key[0]): #对于文本中文list中的每个分词word
                    linescore=linescore+0.8*len(key_list);
                    keyflag=0;

            # 对于文本中文list中的每个分词word
            # 对于问题中文list中的每个分词keyword
            # 获取问题中的关键字及其对应的分数字典scoredict
            #根据其他关键字给这一行文本加分
            temp=test.getScore(keyword,word,scoredict.get(keyword));

            if(scoresum[keyword]<temp):
                scoresum[keyword]=temp;

#超过一半之后就不再判断那个关键词
            # if(test.getScore(keyword,word,scoredict.get(keyword))>(scoredict.get(keyword)/2)):
            #     key_list_temp.remove(keyword);



    for keyword in key_list_temp:
        linescore=scoresum[keyword]+linescore;


    w.write(str(linescore));
    w.write('\n');
    line=f.readline();








f.close();
w.close();