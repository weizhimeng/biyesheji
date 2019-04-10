# -***coding=utf-8***-
# 计算余弦相似度
from sklearn.metrics.pairwise import cosine_similarity



def cos_similar(x,y):
    a = [x,y]
    result = cosine_similarity(a)[0][1].round(8)
    return result


def compare(map,value):
    ma = []
    va = []
    for m in map.values():
        ma.append(m)
    for x in map.keys():
        if x in value.keys():
            num = value[x]
        else:
            num = 0
        va.append(num)
    result = cos_similar(ma,va)
    return result

if __name__ == '__main__':
    x = [1,3,2,6]
    y = [2,2,2,4]
    print(cos_similar(x,y))
