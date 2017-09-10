#-*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import copy
import sys
import test
import utiltest



f = open("youwenti",encoding='utf-8');

question=''
line=f.readline();
scoredict={};
key_list=[];
key_tag_list=[];#关键字的TAG
question_tag_list=[];
question_word_list=[];
#储存分数列表，只取前1个
scoresum={};


#存储使用了多少次luis
luistimes=[]
luis = open('luisnum','r', encoding='utf-8')
luistimes.append(int(luis.readline()))
luis.close()

#存储多少行
linenum=1



while line:

    w = open("linescores", 'a');
    sentences=line.split();


#切割每一行
    if(question!=sentences[1]):
        question=sentences[1];
        scoredict=utiltest.keyDict(question);
        key_list=scoredict.keys();
        t1=test.participle(question);
        question_tag_list=test.participle_cixing(t1);
        question_word_list=test.participle_word(t1);
        answer_type = utiltest.problemsort(question,luistimes);
        answer_key = utiltest.problem_key(question);



    key_list_temp=copy.deepcopy(list(key_list));
    content='';
    contentindex=2;
    while(contentindex<len(sentences)):
        content=content+sentences[contentindex];
        contentindex=contentindex+1;




















    # for a in key_list:
    #     print(a.encode('utf8'))

    # print(scoredict);
#测试 content为每一行内容 question为问题

    typeflag=1;
    keyflag=1;
    linescore=0;
    for keyword in key_list_temp:
        scoresum[keyword]=0;
        key_tag_list.append(question_tag_list[question_word_list.index(keyword)]);
    if(answer_type=='nr'):
        if(content.find('为')!=-1):
            delete_weis=content.split('为');
            content="";
            for wei in delete_weis:
                content+=wei;

    result=test.participle(content);
    Wordlist=test.participle_word(result);
    Taglist=test.participle_cixing(result);
    worlist_index=0;
                        #5.24#这个很有问题
            #如果不是问时间地点人物的话，如果里面有时间和地点会扣一点分
    # if(answer_type=='none' and ('ns' in Taglist or 't' in Taglist)):
    #     linescore=linescore-1.1;
    for word in Wordlist:  #对于文本中文list中的每个分词word
        keyword_index=0;
        for keyword in key_list_temp:  #对于问题中文list中的每个分词keyword
            #根据是否符合问题的类型给这一行文本打分
            if(answer_type in Taglist and typeflag==1): #如果文本中的词性list中有问题的类型
                ########################
                # 2017.5.22这里只判断了时间
                #5.22
                ##############################
                if(type(answer_key)==list and utiltest.doubleadd(answer_key,Wordlist,Taglist,answer_type)): #若answer_key为list类型，即问题中有多个表示时间的关键字
                     linescore=linescore+0.8*len(key_list);
                     typeflag=0;
                elif(type(answer_key)!=list):#2017.5.22这里简单的把关键词去掉以判断其他的情况
                    linescore=linescore+0.8*len(key_list);
                    typeflag=0;

            #根据是否含有问题中时间类型的关键字给这一行文本打分
            if(type(answer_key)==list and keyflag==1):
                if(word in answer_key): #对于文本中文list中的每个分词word
                    linescore=linescore+0.8*len(key_list);
                    keyflag=0;

            # 对于文本中文list中的每个分词word
            # 对于问题中文list中的每个分词keyword
            # 获取问题中的关键字及其对应的分数字典scoredict
            #根据其他关键字给这一行文本加分



            temp=test.getScore(keyword,word,scoredict.get(keyword),Taglist[worlist_index],key_tag_list[keyword_index]);
            #只取最大那个词的分数
            if(scoresum[keyword]<temp):
                scoresum[keyword]=temp;
            keyword_index+=1;
#超过一半之后就不再判断那个关键词
            # if(test.getScore(keyword,word,scoredict.get(keyword))>(scoredict.get(keyword)/2)):
            #     key_list_temp.remove(keyword);

        worlist_index+=1;

#把所有词的最高分相加作为一行的分数
    for keyword in key_list_temp:
        linescore=scoresum[keyword]+linescore;


    print('第',linenum,'行')
    linenum=linenum+1

    w.write(str(linescore));
    w.write('\n');
    line=f.readline();



f.close();
w.close();