# -*- coding: utf-8 -*-
import test
import luisTest
#有量词的术语数词
#什么时候作为时间词
problem_category={"数词":['多少','几','多'],
             "地点":['哪里','哪','哪儿'],
             "人名":['谁'],
            "时间":['时候','年','月','日','何时','几时']
             }



def keyDict(sentence):
    noun_scoreInit=1.0;
    verb_scoreInit=1.1;
    result=test.participle(sentence);
    WordList=test.participle_word(result);
    TagList=test.participle_cixing(result);
    DaiciIndex=test.getDaiciIndex(result);
    NounIndexlist=test.getNounIndex(result);
    VerbIndexlist=test.getVerbIndex(result);
    ZhuciIndexlist=test.getZhuciIndex(result);
    scoredict={};
    left=DaiciIndex-1;
    right=DaiciIndex+1;
    noun_left_num=0;#一旦右边的词扫描晚了，右边的名词数量应该与左边的名词相等重要
    noun_right_num=0;
    verb_turn=0;
    noun_turn=0;
    verb_turn=1.1/len(WordList);
    noun_turn=1.0/len(WordList);
    if(verb_turn<0.15):
        verb_turn=0.15;
    if(noun_turn<0.15):
        noun_turn=0.15
    while(left>=0 or right<len(WordList)):
        if(verb_scoreInit<0.1):
            verb_scoreInit=0.1;
        if(noun_scoreInit<0.1):
            noun_scoreInit=0.1;

        if(right in VerbIndexlist):
            if(len(WordList[right])!=1):
                scoredict[WordList[right]]=verb_scoreInit;
                right=right+1;
                verb_scoreInit=verb_scoreInit-verb_turn;
            else:
                scoredict[WordList[right]]=0.5;
                right=right+1;
                verb_scoreInit=verb_scoreInit-verb_turn;
        elif(left in VerbIndexlist):
            if(len(WordList[left])!=1):
                scoredict[WordList[left]]=verb_scoreInit;
                left=left-1;
                verb_scoreInit=verb_scoreInit-verb_turn;
            else:
                scoredict[WordList[left]]=0;
                left=left-1;
                verb_scoreInit=verb_scoreInit-verb_turn;
        elif(right in NounIndexlist):
            scoredict[WordList[right]]=noun_scoreInit;
            right=right+1;
            noun_scoreInit=noun_scoreInit-noun_turn;
            noun_right_num+=1;
        elif(left in NounIndexlist and (right<len(WordList)or noun_left_num<=noun_right_num)):  #有可能右边一个名词都没有
            scoredict[WordList[left]]=noun_scoreInit;
            left=left-1;
            noun_scoreInit=noun_scoreInit-noun_turn;
            noun_left_num+=1;
        elif(left in NounIndexlist and right>=len(WordList)and noun_left_num>noun_right_num):
            scoredict[WordList[left]]=noun_scoreInit;
            noun_scoreInit=noun_scoreInit-noun_turn*2;


            left=left-1;
        else:
            left=left-1;
            right=right+1;

    return scoredict;

#问题的分类
def problemsort(sentence,luistimes):
    result=test.participle(sentence);
    WordList=test.participle_word(result);
    TagList=test.participle_cixing(result);
    answer='';

    for shuci in problem_category.get('时间'):
        if(shuci in WordList):
            answer='t';
            return answer;
        #如果存在量词，那么它就是数词
    if('q' in TagList):
        answer='m';
        return answer;
    for shuci in problem_category.get('数词'):
        if(shuci in WordList):
            answer='m';
            return answer;
    for shuci in problem_category.get('地点'):
        if(shuci in WordList):
            answer='ns';
            return answer;
    for shuci in problem_category.get('人名'):
        if(shuci in WordList):
            answer='nr';
            return answer;


    # if(luistimes[0] <= 990):
    #     luistimes[0] = luistimes[0] + 1;
    #     print('第 ',luistimes[0],'次使用luis')
    #     f = open('luisnum', 'w', encoding='utf-8')
    #     f.write(str(luistimes[0]))
    #     f.close()
    #     return luisTest.luisQuestion(sentence)

    answer='none';
    return answer



def problem_key(sentence):
    result=test.participle(sentence);
    WordList=test.participle_word(result);
    TagList=test.participle_cixing(result);
    answer='';
    if('t'in TagList):
        a=0;
        answer=[];
        #5.26有可能这个时间词是年月日所有找出所有
        while(a<len(TagList)):
            if(TagList[a]=='t'):
                answer.append(WordList[a]);
            a+=1;
        return answer;
    answer='none';
    return answer

#判断文本中是否含有除了问题中时间关键字以外的其他时间性词汇
#用来处理时间性词汇因为符合问题类型和关键字同时加了两次分的问题
def doubleadd(answerkey,wordlist,taglist,type):
    for i in answerkey: #对于每一个时间关键词
        for j,t in enumerate(wordlist): #对于文本中的每一个word
            if taglist[j] == type : #如果这个word的标记是时间t
                if t != i: #并且这个word和时间关键字不相等
                    #print(True)
                    return True #那么返回true表示可以加分

    #print(False)#否则表示不能够加分
    return False


