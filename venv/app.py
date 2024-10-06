import math
import os
from collections import Counter

from config import game_num, data, ban
from flask import Flask, render_template

app = Flask(__name__)

path = './venv/static/game'
gameList = os.listdir(path)

teamList = [['잉규', 'TT', '종혁', '숙희', 'Iris'], ['항상화가남', '트루스틱', '구름', '게이', '아로'],
            ['망고', '초코', '재우', '켈룬', '산간고'], ['HIT', 'CK', 'SH', '정익', '트랜스젠더'],
            ['애리', '치껍', '알파', '낙붕오', 'Explozion'], ['크림', 'Dopa', 'Roger', '포칩', '매국노'],
            ['승훈겅듀헿', 'Magarine', '카키', 'Hello', '시안'], ['TH', '산', '박쥐', 'Jfla', '다중이'],
            ['치킨', '필씅', 'Valme', '믹키재원', '유부'], ['코첼', '위너', 'newprojin', 'Haibe', 'Asp']]
leaderList = [i[0] for i in teamList]

table = [["" for j in range(10)] for i in range(10)]
for i in range(10):
    table[i][i] = '◈'
screenshotList = [[], [], [], [], [], [], [], [], [], []]
for i in gameList:
    spl = i[0:-4].split(' ')
    print(spl)
    table[leaderList.index(str(spl[1]))][leaderList.index(str(spl[3]))] = '승'
    table[leaderList.index(str(spl[3]))][leaderList.index(str(spl[1]))] = '패'
    screenshotList[leaderList.index(str(spl[1]))].append(i)
    screenshotList[leaderList.index(str(spl[3]))].append(i)
print(table)
print(screenshotList)
win = []
for m in table:
    x, y = 0, 0
    for n in m:
        if n == '승':
            x += 1
        elif n == '패':
            y += 1
    win.append([x, y])

member = []
for i in teamList:
    member = member + i
# print(member)
clanDic = dict.fromkeys(member)
for i in clanDic:
    clanDic[i] = {'c': [], 'k': [], 'd': [], 'a': [], 's': [], 'cc': None, 'ave': None, 'max': None, 'kda': None}
    # print(clanDic)
for i in data:
    clanDic[i[0]]['c'].append(i[1])
    clanDic[i[0]]['k'].append(i[2])
    clanDic[i[0]]['d'].append(i[3])
    clanDic[i[0]]['a'].append(i[4])
    clanDic[i[0]]['s'].append(i[5])
for i in data:
    clanDic[i[0]]['cc'] = Counter(clanDic[i[0]]['c']).most_common()
    clanDic[i[0]]['ave'] = math.ceil((sum(clanDic[i[0]]['s'])) / len(clanDic[i[0]]['s']))
    clanDic[i[0]]['max'] = max(clanDic[i[0]]['s'])
    clanDic[i[0]]['kda'] = round((sum(clanDic[i[0]]['k']) + sum(clanDic[i[0]]['a'])) / sum(clanDic[i[0]]['d']), 2)
# print(clanDic)

banList = []
for i in leaderList:
    banList.append(Counter(ban[i]).most_common(10))
total = []
total_pick, total_ban = [], []
for i in leaderList:
    total = total + ban[i]
    total_ban += ban[i]

for i in member:
    total = total + clanDic[i]['c']
    total_pick += clanDic[i]['c']
tierList = Counter(total).most_common(20)
# print(tierList)
tier_pick = Counter(total_pick).most_common()
tier_ban = Counter(total_ban).most_common()
# print(tier_pick)
# print(tier_ban)
pick_cnt, ban_cnt = [], []
for i in tierList:
    for j in tier_pick:
        if i[0] == j[0]:
            pick_cnt.append(j[1])
    for j in tier_ban:
        if i[0] == j[0]:
            ban_cnt.append(j[1])

max_k,max_id=[],[]
for i in clanDic:
    max_k.append(sum(clanDic[i]['k']))
    max_id.append([i,sum(clanDic[i]['k'])])
print(max_k)
print(sorted(max_k))
print(max_id)
max_a,max_aid=[],[]
for i in clanDic:
    max_a.append(sum(clanDic[i]['a']))
    max_aid.append([i,sum(clanDic[i]['a'])])
print(max_a)
print(sorted(max_a))
print(max_aid)

visitor_cnt = 0


@app.route('/')
def index():
    global visitor_cnt
    visitor_cnt += 1
    print('visitor_cnt: ', visitor_cnt)
    return render_template('index.html', teamList=teamList, leaderList=leaderList, table=table, win=win,
                           screenshotList=screenshotList, clanDic=clanDic, banList=banList, tierList=tierList,
                           game_num=game_num, pick_cnt=pick_cnt, ban_cnt=ban_cnt)


if __name__ == '__main__':
    app.run(debug=True)
