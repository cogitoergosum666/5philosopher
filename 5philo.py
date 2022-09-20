# 五个哲学家例程
# 五个哲学家围绕着桌子坐下，每个哲学家两侧有一只筷子，哲学家只会处于思考或进食状态，求一定时间内同时进食的哲学家数量最大的最优解
# 进食需要3s

from cmath import acos, asin, log, pi, sin, sqrt
from errno import EEXIST
from math import cos, degrees, radians , asin , sin , acos, tan
import random
from re import I
from secrets import choice
from time import sleep
from sympy import *
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_circle(center=(3, 3),r=2):

    x = np.linspace(center[0] - r, center[0] + r, 5000)

    y1 = np.sqrt(r**2 - (x-center[0])**2) + center[1]

    y2 = -np.sqrt(r**2 - (x-center[0])**2) + center[1]

    plt.plot(x, y1, c='k')

    plt.plot(x, y2, c='k')

    #plt.show()

class PhilosopherTable:
    def __init__(self,t):
        self.Status = [0,0,0,0,0] #哲学家状态，为0为思考，为1为进食
        self.Chopsticks = [[0,0],[0,0],[0,0],[0,0],[0,0]] #显示每个哲学家两侧筷子状态，前者为左侧（顺时针），后者为右侧（逆时针）
        self.TimeCount = [0,0,0,0,0]#计时
        self.Timepass = t

    def Chop_sysn(self,p,v):
        # for i in range(len(self.Chopsticks)):
        #     if self.Chopsticks[i][0] == 1:
        #         self.Chopsticks[(i-1)%5][1] = 1
        #     if self.Chopsticks[i][1] == 1:
        #         self.Chopsticks[(i+1)%5][0] = 1
        #     if self.Chopsticks[i][0] == 0:
        #         self.Chopsticks[(i-1)%5][1] = 0
        #     if self.Chopsticks[i][1] == 0:
        #         self.Chopsticks[(i+1)%5][0] = 0
        self.Chopsticks[p][0] = self.Chopsticks[p][1] = self.Chopsticks[(p+1)%5][1] = self.Chopsticks[(p-1)%5][0] = v
        

    def ChangeStatus(self,p,f):
        if self.Status[p] == 1 and self.TimeCount[p] == 0:
            self.Status[p] = 0
            self.Chop_sysn(p,0)
            f.write("第" + str(self.Timepass) + "秒时：第" + str(p) + "号哲学家进食结束，转换为思考状态\n")
        else:
            if self.Status[p] == 0 and self.Chopsticks[p][0] == 0 and self.Chopsticks[p][1] == 0 : 
                self.Status[p] = 1
                
                self.TimeCount[p] = 3
                self.Chop_sysn(p,1)
                f.write("第" + str(self.Timepass) + "秒时：第" + str(p) + "号哲学家试图进食，条件满足，进食成功\n")
                return p
            else:
                f.write("第" + str(self.Timepass) + "秒时：第" + str(p) + "号哲学家试图进食，但因为没有筷子失败，继续思考\n")
    
    def Eating(self,p,f):
        self.TimeCount[p] -= 1
        if self.TimeCount[p] == 0:
            self.ChangeStatus(p,f)
        else:
            f.write("第" + str(self.Timepass) + "秒时：第" + str(p) + "号哲学家正在进食，已经进食" + str(3 - self.TimeCount[p])+"秒\n")

    def Draw(self,count):
        plt.figure(figsize=(10,10))
        px = np.array([])
        py = np.array([])
        for i in range(0,360,72):
            px = np.append(px,np.cos((i/180)*np.pi)*10)
            py = np.append(py,np.sin((i/180)*np.pi)*10)
        color = []
        for guys in self.Status:
            if guys == 1:
                color.append("red")
            else:
                color.append("green")
        colors = np.array(color)
        #colors = np.array(["red","green","black","orange","purple","beige","cyan","magenta"])
        plt.scatter(px,py,1000,c=colors)
        plot_circle((0,0),r=10)
        plt.savefig('log'+str(count) + '.png')


def LoadConfig():
        with open('config.txt','r+') as f:
            count = int(f.readline())
            count += 1
            f.truncate(0)
            f.seek(0)
            f.write(str(count))
            f.close()
        return count



def main():
    count = LoadConfig()
    os.mkdir('log'+str(count))
    os.chdir('log'+str(count))
    with open('log' + str(count) + '.txt','w+') as f:
        f.write('****************************这是第'+str(count)+'个日志****************************\n\n')
        table = PhilosopherTable(0)
        #table.Draw()
        queue = [0,1,2,3,4]
        while(1) : 
            for i in range(len(table.Status)):
                if table.Status[i] == 1:
                    table.Eating(i,f)
            eating = []
            eating1 = []
            for i in queue:
                eating.append(table.ChangeStatus(i%5,f))
            #eating1 = list(filter(None,eating))
            for i in eating:
                if i is not None:
                    eating1.append(i)
            for i in range(len(eating1)):

                queue.remove(eating1[i])
                queue.append(eating1[i])

            table.Draw(table.Timepass)
            table.Timepass += 1
            


            if table.Timepass == 20 : 
                break 

        f.close()

if __name__ == '__main__':
    main()



