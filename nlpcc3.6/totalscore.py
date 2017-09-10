#-*- coding: utf-8 -*-
import copy
import sys


#根据传入的list和index计算出rank值
#根据传入的list和index计算出rank值
def cal_rank(allscore_list,answer_index):

    #按照分数对[行号，分数]对降序排列
    allscore_list.sort(key=lambda x: x[1], reverse=True)
    #记录真正的位置（重复的算作一位）
    count=1

    #找到答案所在的couple的下标，count就是对应的rank值
    for index, value in enumerate(allscore_list):

        if index == 0 :
            if value[0] == answer_index:
                return 1
            continue

        #假如现在的分数和上一个一样，那么不增加count，进行下标的判断并返回
        if value[1] == allscore_list[index-1][1]:

            #如果是答案，则返回count
            if value[0] == answer_index:
                return count
            else:
                continue

        # 现在的分数和上一个不一样
        else:
            #增加count
            count=count+1
            #判断是不是答案
            if value[0] == answer_index:
                return count


#为了存储总的questionnumber和allrank
#q_and_r[0]即allrank   q_and_r[1]为questionnumber
def readscore():
    fenshu = open('fenshu',encoding='utf-8')
    fenshuline = fenshu.readline();
    q_and_r = [];

    while fenshuline:
        q_and_r.append(float(fenshuline))
        fenshuline = fenshu.readline();

    return q_and_r[0],int(q_and_r[1])


#将allrank和questionnumber写会fenshu文件中
def writescore(allrank,questionnumber):
    w = open("fenshu", 'w');
    w.write(str(allrank))
    w.write('\n')
    w.write(str(questionnumber))


f = open("youwenti",encoding='utf-8');
w=open("linescores",encoding='utf-8');
question=''
line=f.readline();
linescore = float(w.readline())


allrank,questionnumber = readscore()

rank=0
count=1
answer_index=0 #存储答案是位于第几个文本，从1开始
allscore=[] #存储每一行对应的分数
line_score_couple=[0,0]
#行数
linenumber=1;


newquestion=(line.split())[1]


while line:

    linenumber+=1;
    sentences=line.split();

    #假如是一个新的问题
    #计算上一轮的rank并进行初始化
    if(newquestion != sentences[1]):

        rank = cal_rank(allscore, answer_index) #计算上一轮的rank
        if(rank != None):
            allrank = allrank + (1/rank)
        newquestion=sentences[1]
        questionnumber=questionnumber+1
        print('di ',questionnumber,' gewentide  rank:',rank)

        rank = 0
        count = 1
        answer_index = 0  # 存储答案是位于第几个文本，从1开始
        allscore=[] # 存储每一行对应的分数
        line_score_couple = [0, 0]

    if(sentences[0] == '1'):
        answer_index = count


    #去拿每一行的分数
    line_score_couple[1]=float(linescore)
    line_score_couple[0]=count
    allscore.append(copy.deepcopy(line_score_couple))
    count = count + 1

    line=f.readline();
    linescore=w.readline()




#计算最后一轮的rank
rank = cal_rank(allscore, answer_index)
if(rank != None):
    allrank = allrank + (1.0/rank)

questionnumber=questionnumber+1

writescore(allrank,questionnumber)

# allscore.sort(key=lambda x: x[1], reverse=True)
# print(allscore)
print('di ',questionnumber,' gewentide  rank:',rank)
print(allrank/questionnumber)

f.close();
w.close();