import random
import matplotlib.pyplot as plt 
colors=['black', 'blue', 'green', 'red', 'yellow', 'orange','purple', 'darkblue','lightblue','gold', 'lime', 'maroon',
            'olive', 'silver', 'orchid', 'salmon', 'tomato', 'yellowgreen', 'rosybrown', 'plum', 'peru', 'tan', 'sienna', 'saddlebrown',
            'palevioletred']
TEST_CASE = ([(5, 13), (10, 5), (11, 9), (18, 9), (8, 3), (0, 10), (19, 17), (9, 17), (11, 12), (18, 3), (3, 4), (17, 11), (5, 2), (6, 12), (18, 7), (1, 7), (11, 4), (13, 1), (6, 15), (0, 3), (19, 2), (18, 10), (14, 1), (16, 3), (4, 3), (3, 15), (19, 11), (13, 13), (4, 4), (2, 9), (15, 7), (2, 15), (7, 18), (13, 14), (14, 0), (15, 15), (17, 3), (13, 16), (15, 9)], 
                        [11, 7, 2, 21, 11, 16, 6, 21, 9, 8, 9, 24, 23, 0, 6, 17, 18, 18, 5, 15, 4, 10, 12, 24, 12, 7, 20, 22, 3, 11, 19, 0, 4, 14, 13, 21, 1, 12, 9])
def TestCaseGenerate(citynum : int, typenum : int, scaleMax: int = 100, seed = None):
    assert citynum >= typenum
    if(seed):
        random.seed(seed)
    cities = []
    typeList = list(range(typenum))
    while len(cities) < citynum:
        x = random.randint(0,scaleMax)
        y = random.randint(0,scaleMax)
        if((x,y) in cities):
            continue
        cities.append((x,y))

    for _ in range(citynum - typenum):
        typeList.append(random.randint(0, typenum-1))
    random.shuffle(typeList)
    return cities, typeList

##### 绘图 #####
def PltResult(cityList, typeList, solution):
    for i in range(len(cityList)):
        (x,y) = cityList[i]
        color = colors[typeList[i]]
        plt.scatter(x, y, label='Location', color = color)

    solutionX = [pos[0] for pos in solution]
    solutionY = [pos[1] for pos in solution]

    solutionX.append(solutionX[0])
    solutionY.append(solutionY[0])
    plt.plot(solutionX, solutionY, label = 'result', color = 'black', alpha = 0.2, marker = '*', 
             linewidth = 2, markersize=16) # 路径
    plt.ylabel("Y")
    plt.xlabel("X")
    plt.title("Final Result")
    plt.show()

def PltProcess(historyBestValues):
    plt.plot(historyBestValues)
    plt.title("best value")
    plt.ylabel("path cost")
    plt.xlabel("t")
    plt.show()
