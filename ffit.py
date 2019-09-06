import numpy as np
import math
import matplotlib.pyplot as plt

def fourierCalc(x, npa, npb, n):
    sum = 0
    for i in range(0,n):
        f = 2*math.pi*(i+1)
        sum += npa[i]*math.cos(f*(x-npb[i]))
    return sum

def fourierSeries(npx, npa, npb, n):
    npy = np.zeros(len(npx))
    for i,x in enumerate(npx):
        npy[i] = fourierCalc(x, npa, npb, n)
    return npy

def calcRMSErr(npx, npy, fity):
    n = len(npx)
    result = np.zeros(n)
    for i in range(0, n):
        err = fity[i] - npy[i]
        result[i] = err**2
    mean = np.mean(result)
    return math.sqrt(mean)

def isthereabetterfitb(npx, npy, npa, npb, n, i, iterationsdesired,cerr):
    currb = npb[i]
    for k in range(0, iterationsdesired):
        npb[i] = npb[i] + 0.15
        yfit = fourierSeries(npx, npa, npb,n)
        newerr = calcRMSErr(npx, npy,yfit)
        if newerr < cerr:
            currb = npb[i]
    return currb

def isthereabetterfita(npx, npy, npa, npb, n, i, iterationsdesired,cerr):
    curra = npa[i]
    besthigh = curra
    higherr = cerr
    bestlow = curra
    lowerr = cerr
    for k in range(0, iterationsdesired):#find higher
        npa[i] = npa[i] + 0.08*npa[i]
        yfit = fourierSeries(npx, npa, npb,n)
        newerr = calcRMSErr(npx, npy,yfit)
        if newerr < cerr:
            besthigh = npa[i]
            higherr = newerr
    
    for k in range(0, iterationsdesired):#find higher
        npa[i] = npa[i] - 0.08*npa[i]
        yfit = fourierSeries(npx, npa, npb,n)
        newerr = calcRMSErr(npx, npy,yfit)
        if newerr < cerr:
            bestlow = npa[i]
            lowerr = newerr

    if lowerr <= higherr:
        curra = bestlow
    else:
        curra = besthigh
    return curra

def printResults(npa, npb, chi):
    n = len(npa)
    print("fitted", n, "order series...")
    print("equation is:")
    eqn = "y = "
    for i in range(0, n):
        fa = 2*(i+1)
        f = str(fa)+"pi"
        if npb[i] >=0:
            bstr = "- " + str(npb[i])
        else:
            bstr = "+ " + str(npb[i])
        if i > 0:
            if npa[i] >=0:
                strt = " + "
            else:
                strt = ""
        else:
            strt = ""
        strt += str(npa[i])+"cos(" + f + "(x " + bstr + "))"
        eqn += strt
    print(eqn)
    print("-------------")
    print("error:", chi)


def attemptFit(npx, npy, n, iterationsdesired=100):
    npa = np.ones(n)
    npb = np.zeros(n)
    for i in range(0, n):
        npa[i] = npy[0]#just set at this to start
    #we start here
    fity = fourierSeries(npx, npa,npb, n)
    chisqr = calcRMSErr(npx, npy, fity)
    for k in range(0, 3):
      for i in range(0, n): #let us go by term 1 first
        for j in range(0, 3):
            npa[i] = isthereabetterfita(npx, npy, npa, npb, n, i, iterationsdesired, chisqr)
            fity = fourierSeries(npx, npa,npb, n)
            chisqr = calcRMSErr(npx, npy, fity)
            npb[i] = isthereabetterfitb(npx, npy, npa, npb, n, i, iterationsdesired, chisqr)
            fity = fourierSeries(npx, npa,npb, n)
            chisqr = calcRMSErr(npx, npy, fity)
            #print(npa, npb[i])

    printResults(npa,npb, chisqr)
    return fity, chisqr, npa, npb

def test():
    x = np.linspace(0, 8, 100)
    y = np.sin(2*math.pi*(x-0.5))
    y += np.cos(4*math.pi*(x-0.8))
    y += np.random.rand(100)/7
    y += np.random.rand(100)/7
    y += np.random.rand(100)/7

    fity, err, npa, npb = attemptFit(x,y,5,500)
    plt.plot(x, y)
    plt.plot(x, fity)
    plt.show()
