import random
import turtle as t

"""soprano = [5]
tenor = [8]
alto = [3]"""


def genSoprano(bassLine, startPitch):
    print("Creating the soprano line...")
    sopranoLine = bassLine[:]
    sopranoLine[0] = startPitch
    i = 1
    while i < len(bassLine):
        options = [bassLine[i] - 7, bassLine[i] - 5, bassLine[i] - 3, bassLine[i], bassLine[i] + 2, bassLine[i] + 4,
                   bassLine[i] + 7]
        if bassLine[i] > bassLine[i - 1]:
            options = filterGreaterThan(options, sopranoLine[i - 1])
            options = filterJumps(options, sopranoLine[i - 1])
            if parallel5(bassLine[i-1], sopranoLine[i-1]):
                if bassLine[i] + 4 in options:
                    options.remove(bassLine[i]+4)
                if bassLine[i] -3 in options:
                    options.remove(bassLine[i]-3)
            options = filterRange(4, 11, options)
            sopranoLine[i] = options[random.randint(0, len(options) - 1)]
        else:
            options = filterLessThan(options, sopranoLine[i - 1])
            options = filterRange(4, 11, options)
            options = filterJumps(options, sopranoLine[i - 1])
            if parallel5(bassLine[i-1], sopranoLine[i-1]):
                if bassLine[i] + 4 in options:
                    options.remove(bassLine[i]+4)
                if bassLine[i] -3 in options:
                    options.remove(bassLine[i]-3)
            options = filterRange(4, 11, options)
            sopranoLine[i] = options[random.randint(0, len(options) - 1)]
        i += 1
    print("Done.")
    return sopranoLine



def genAltoTenor(bassLine, sopranoLine, startPitchA, startPitchT):
    altoLine = bassLine[:]
    tenorLine = bassLine[:]
    #set start pitch
    altoLine[0] = startPitchA
    tenorLine[0] = startPitchT
    i = 1
    while i < len(bassLine):
        #create options
        options = [bassLine[i] - 7, bassLine[i] - 5, bassLine[i] - 3, bassLine[i], bassLine[i] + 2, bassLine[i] + 4,
                   bassLine[i] + 7]
        options = removeNote(sopranoLine[i], options)
        options = removeNote(bassLine[i], options)
        if sopranoLine[i]%7 == bassLine[i]:
            #soprano has already doubled bass.
            #pick an option for each
            if altoLine[i-1] in options:
                altoLine[i] = altoLine[i-1]
            elif tenorLine[i-1] in options:
                tenorLine[i] = tenorLine[i-1]
            third = [bassLine[i] + 2,  bassLine[i] -3]
            fifth = [bassLine[i] + 4, bassLine[i] - 5]
            if min(abs(third[0] - tenorLine[i-1]), abs(third[1] - tenorLine[i-1])) < min(abs(third[0] - tenorLine[i-1]), abs(third[1] - tenorLine[i-1])):
                tenorLine[i] = findSmallestInt(third, tenorLine[i-1])
                altoLine[i] = findSmallestInt(fifth, altoLine[i-1])
            else:
                altoLine[i] = findSmallestInt(third, altoLine[i-1])
                tenorLine[i] = findSmallestInt(fifth, tenorLine[i-1])
        else:
            #soprano hasnt doubled the bass. this note will be given to the part with the shortest interval
            if abs(bassLine[i] - altoLine[i-1]) > abs(bassLine[i] - tenorLine[i-1]):
                tenorLine[i] = bassLine[i]
                altoLine[i] = findSmallestInt(options, altoLine[i-1])
            else:
                altoLine[i] = bassLine[i]
                tenorLine[i] = findSmallestInt(options, tenorLine[i-1])
        i += 1
    return altoLine, tenorLine


def filterLessThan(list, val):
    i = 0
    while i < len(list):
        if list[i] < val:
            while list[i] < val:
                list[i] = list[i] + 7
        i += 1
    return list


def filterGreaterThan(list, val):
    i = 0
    while i < len(list):
        if list[i] > val:
            while list[i] > val:
                list[i] = list[i] - 7
        i += 1
    return list


def filterJumps(ops, sVal):
    i = 0
    while i < len(ops):
        if abs(ops[i] - sVal) > 5:
            ops.pop(i)
            i -= 1
        i += 1
    return ops


def findSmallestInt(list, val):
    i = 1
    index = 0
    min = abs(list[0] - val)
    secondMin = abs(list[0] - val)
    secondIndex = 0
    while i < len(list):
        if abs(list[i] - val) < min:
            min = abs(list[i] - val)
            index = i
        elif abs(list[i] - val) == min:
            secondMin = abs(list[i] - val)
            secondIndex = i
        i += 1
    if not secondIndex == 0:
        a = random.randint(0,1)
        if a == 0:
            return list[index]
        else:
            return list[secondIndex]
    else:
        return list[index]


def parallel5(b,s):
    if s < b:
        temp = b-7
        if abs(s-temp)==4:
            return True
        else:
            return False
    else:
        if abs(s-b)==4:
            return True
        else:
            return False

def removeNote(n, l):
    if n in l:
        l.remove(n)
    if n + 7 in l:
        l.remove(n+7)
    if n - 8 in l:
        l.remove(n-8)
    return l

def filterRange(a,b,l):
    i = 0
    while i < len(l)-1:
        if l[i] < a:
            l[i] = l[i]+7
        if l[i] > b:
            l[i] = l[i]-7
        i += 1
    return l


def drawStaff():
    t.speed(0)
    for i in range(5):
        t.up()
        t.goto(-400, 200 - 20 * i)
        t.down()
        t.forward(800)
    for i in range(5):
        t.up()
        t.goto(-400, -25 - 20 * i)
        t.down()
        t.forward(800)
        t.up()


def drawNotes(notes, startPos):
    radius = 10
    for i in range(len(notes)):
        xPos = -300+75*i
        yPos = startPos+10*(notes[i]-1)
        if startPos > 0 and yPos <= 90 or yPos >= 210:
            t.up()
            t.goto(xPos-4, yPos+10)
            t.down()
            t.width(5)
            t.goto(xPos+24, yPos+10)
            t.width(1)
        if startPos < 0 and yPos >= -15:
            t.up()
            t.goto(xPos - 4, yPos + 10)
            t.down()
            t.width(5)
            t.goto(xPos + 24, yPos + 10)
            t.width(1)
        t.up()
        t.goto(xPos+radius,yPos)
        t.down()
        t.begin_fill()
        t.circle(radius)
        t.end_fill()


if __name__ == "__main__":
    bass = [8, 6, 2, 5, 8]
    soprano = genSoprano(bass, 5)
    alto, tenor = genAltoTenor(bass, soprano, 3, 8)
    print(soprano)
    print(alto)
    print(tenor)
    print(bass)
    drawStaff()
    drawNotes(soprano, 90)
    drawNotes(alto, 90)
    drawNotes(tenor, -85)
    drawNotes(bass, -155)
    t.exitonclick()



