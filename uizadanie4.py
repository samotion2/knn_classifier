import matplotlib.pyplot as plt
from random import randint
from time import time
from multiprocessing import Process, Pool
from operator import itemgetter

class Point: #trieda, ktora uchovava suradnice a farbu bodu
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
    
    def __str__(self):
        return str(self.x) + str(self.y) + self.color
    
    def setColor(self, color):
        self.color = color

def classify(x, y, k, arr): #funkcia na klasifikaciu bodu
    z = k - 1
    sus = [(15000, 'r')]*k #array k najblizsich susedov

    for i in arr: #prejde sa array a najde sa k najblizsich bodov
        temp = abs(x - i.x) + abs(y - i.y) #manhattanovska vzdialenost
        if temp < sus[k - 1][0]:#vzdialenost sa porovna s poslenym prvkom ak je mensia postupne prebublava nizsie
            while ((z > 0) and (temp < sus[z - 1][0])):
                z -= 1

            sus.pop()
            sus.insert(z, (temp, i.color))

            z = k - 1 

    distance = [[0, 0, 'r'], [0, 0, 'g'], [0, 0, 'b'], [0, 0, 'purple']]
    
    for i in range(k): #spocitanie farbieb a vzdialenosti najblizsich susedov
        if sus[i][1] == 'r':
            distance[0][0] += 1
            distance[0][1] += sus[i][0]
        elif sus[i][1] == 'g':
            distance[1][0] += 1
            distance[1][1] += sus[i][0]
        elif sus[i][1] == 'b':
            distance[2][0] += 1
            distance[2][1] += sus[i][0]
        elif sus[i][1] == 'purple':
            distance[3][0] += 1
            distance[3][1] += sus[i][0]
            
    distance = sorted(distance, key = lambda x: (x[0], -x[1])) #ak je pocet susedov rovnaky berie sa do uvahu kratsia vzdialenost
    return distance[3][2] #vrati farbu najblizsich k susedov

def coordinates(minx, maxx, miny, maxy, a): #vygeneruje nahodny bod v danom intervale a zabezpeci aby bol unikatny
    x = randint(minx, maxx)
    y = randint(miny, maxy)
    while (x, y) in a:
        x = randint(minx, maxx)
        y = randint(miny, maxy)
    return(x, y)

def initarr(num, a): # vygeneruje array suradnic postupne vzdy postupne generuje body pre R, G, B, a P
    arr = []
    for i in range(num // 4):
        if rand(): #R
            x, y = coordinates(-5000, 5000, -5000, 5000, a)
        else:
            x, y = coordinates(-5000, 500, -5000, 500, a) 
        a.add((x, y))
        arr.append((x, y))
        
        if rand(): #G
            x, y = coordinates(-5000, 5000, -5000, 5000, a)
        else:
            x, y = coordinates(-500, 5000, -5000, 500, a)
        a.add((x, y))
        arr.append((x, y))

        if rand(): #B
            x, y = coordinates(-5000, 5000, -5000, 5000, a)
        else:
            x, y = coordinates(-5000, 500, -500, 5000, a)
        a.add((x, y))
        arr.append((x, y))

        if rand(): #P
            x, y = coordinates(-5000, 5000, -5000, 5000, a)
        else:
            x, y = coordinates(-500, 5000, -500, 5000, a) 
        a.add((x, y))
        arr.append((x, y))
    return arr

def rand(): #1%, ze funkcia vrati true
    if randint(0,99) == 99:
        return True
    else:
        return False

def init(): #inicializacia pociatocnych bodov
    red = [(-4500, -4400), (-4100, -3000), (-1800, -2400), (-2500, -3400), (-2000, -1400)]
    green = [(4500, -4400), (4100, -3000), (1800, -2400), (2500, -3400), (2000, -1400)]
    blue = [(-4500, 4400), (-4100, 3000), (-1800, 2400), (-2500, 3400), (-2000, 1400)]
    purple =[(4500, 4400), (4100, 3000), (1800, 2400), (2500, 3400), (2000, 1400)]
    arr = []

    for i in red:
        temp = Point(i[0],i[1])
        temp.setColor('r')
        arr.append(temp)

    for i in green:
        temp = Point(i[0],i[1])
        temp.setColor('g')
        arr.append(temp)

    for i in blue:
        temp = Point(i[0],i[1])
        temp.setColor('b')
        arr.append(temp)

    for i in purple:
        temp = Point(i[0],i[1])
        temp.setColor('purple')
        arr.append(temp)
    return arr

def sucrate(arr, num): #funkcia, ktora vyhodnoti uspesnost klasifikatora
    r, g, b, p = 0, 0, 0, 0

    for i in range(20, len(arr), 4):
        if arr[i].color == 'r':
            r += 1
        if arr[i + 1].color == 'g':
            g += 1
        if arr[i + 2].color == 'b':
            b += 1
        if arr[i + 3].color == 'purple':
            p += 1
    perc = lambda x: 100/num*x/25*100
    print('Red: {:.2f}%, Green: {:.2f}%, Blue: {:.2f}%, Purple: {:.2f}, Overall: {:.2f}%'.format(perc(r), perc(g), perc(b), perc(p), 100/num*r+100/num*g+100/num*b+100/num*p)) 

def main(num, k, pts):
    start = time()
    
    arr = init()
    for i in range(num): #klasifikacia bodov
        r1, r2 = pts[i][0], pts[i][1]

        color = classify(r1, r2, k, arr)
        temp = Point(r1, r2)
        temp.setColor(color)
        arr.append(temp)
    
    sucrate(arr, num) #vypis uspesnosti classifikatora
    back = background(arr, k) #generacia bodov pozadia

    plt.figure(k)
    plt.scatter([i.x for i in back], [i.y for i in back], color = [i.color for i in back], s = 80, alpha = 0.2, marker = '8')#pozadie
    plt.scatter([i.x for i in arr], [i.y for i in arr], color = [i.color for i in arr], s = 36, edgecolor = 'black')#body vpredu
    
    print('Cas vykonania: {:.2f}s K-{}'.format(time() - start, k))
    plt.axis([-5000, 5000, -5000, 5000])
    plt.title('k = ' + str(k))
    plt.subplots_adjust(left = 0.09, right = 0.99 , bottom = 0.05, top = 0.94)
    plt.show()
    
def func(x1): #klasifikacia bodov na pozadi
    x, y, k, arr = x1
    color = classify(x, y, k, arr)
    temp = Point(x, y)
    temp.setColor(color)
    return temp

def background(arr, k): #vygeneruje body na pozadi
    a = set()
    a.update(arr)
    pool = Pool()

    arr1 = [(x, y, k, arr) for x in range(-5000, 5000, 99) for y in range(-5000, 5000, 99) if (x, y) not in a]
    back = pool.map(func, arr1)
    pool.close()
    pool.join()
    return back

if __name__ == '__main__':
    num = 20020 #pocet bodov, ktore chceme generovat
    a = set() #set na kontrolovanie unikatnych bodov
    pts = initarr(num, a)

    k = [1, 3, 7, 15]
    proc = [Process(target = main, args = (num, i, pts)) for i in k] #pre kazde k sa spusti samostatny proces

    for i in proc:
        i.start()

    for i in proc:
        i.join()

    
