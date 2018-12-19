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
        options = [bassLine[i] - 7, bassLine[i] - 5, bassLine[i] - 3, bassLine[i], bassLine[i] + 2, bassLine[i] + 4, bassLine[i] + 7,
                   bassLine[i]+5, bassLine[i]+2, bassLine[i]-2, bassLine[i]-5]
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
        if sopranoLine%7 == bassLine[i]:
            #soprano has already doubled bass. Remove these options.
            if bassLine[i] - 7 in options:
                options.remove(bassLine[i] - 7)
            if bassLine[i] in options:
                options.remove(bassLine[i])
            if bassLine[i] + 7 in options:
                options.remove(bassLine[i] + 7)
            #pick an option for each
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
                # figure out which note is left and give it to the alto
                if sopranoLine[i] in options:
                    options.remove(sopranoLine[i])
                if sopranoLine[i] - 8 in options:
                    options.remove(sopranoLine[i] -8)
                if sopranoLine[i] + 7 in options:
                    options.remove(sopranoLine[i]+7)
                #remove the bass options too, then let alto pick the smallest interval left
            else:
                altoLine[i] = bassLine[i]
                #figure out which note is left adn give it to the tenor




"""def genAlto(bassLine, sopranoLine, startPitch):
    print("Creating the alto line...")
    altoLine = bassLine[:]
    altoLine[0] = startPitch
    i = 1
    while i < len(bassLine):
        options = [bassLine[i] - 7, bassLine[i] - 5, bassLine[i] - 3, bassLine[i], bassLine[i] + 2, bassLine[i] + 4, bassLine[i] + 7]
        if sopranoLine[i] in options:
            options.remove(sopranoLine[i])
        if sopranoLine[i]%7 == bassLine[i] or abs(bassLine[i] - altoLine[i-1]) > 3:
            print("soprano has already doubled the bass note of " + str(bassLine[i]) +
                 ". Removing option to double bass. Previous options were " + str(options))
            if bassLine[i]-7 in options:
                options.remove(bassLine[i]-7)
            if bassLine[i] in options:
                options.remove(bassLine[i])
            if bassLine[i]+7 in options:
                options.remove(bassLine[i]+7)
            if altoLine[i-1] in options:
                altoLine[i] = altoLine[i-1]
            print("options list is: " + str(options) + ". soprano line at this index is " + str(sopranoLine[i]))
            k = 0
            while k < len(options)-1:
                if options[k] > sopranoLine[i]:
                    print("adjusted value " + str(options[k]))
                    options[k] = options[k]-7
                k += 1
            options = filterJumps(options, altoLine[i-1])
            print(str(options))
            #options = filterRange(-1, 6, options)
            altoLine[i] = findSmallestInt(options, altoLine[i - 1])
        else:
            if sopranoLine[i] <= bassLine[i]:
                altoLine[i] = bassLine[i]-7
            else:
                altoLine[i] = bassLine[i]
        i += 1
    print("Done.")
    return altoLine


def genTenor(bassLine, sopranoLine, altoLine, startPitch):
    print("Creating tenor line...")
    tenorLine = bassLine[:]
    tenorLine[0] = startPitch
    i = 1
    while i < len(bassLine):
        options = [bassLine[i] - 7, bassLine[i] - 5, bassLine[i] - 3, bassLine[i] + 2, bassLine[i] + 4, bassLine[i] + 7]
        if sopranoLine[i] in options:
            options.remove(sopranoLine[i])
        if altoLine[i] in options:
            options.remove(altoLine[i])
        if sopranoLine[i]%7 == bassLine[i] or altoLine[i]%7 == bassLine[i] or sopranoLine[i] == bassLine[i] or altoLine[i] == bassLine[i] or abs(bassLine[i] - altoLine[i-1]) > 3:
            if bassLine[i]-7 in options:
                options.remove(bassLine[i]-7)
            if bassLine[i] in options:
                options.remove(bassLine[i])
            if bassLine[i]+7 in options:
                options.remove(bassLine[i]+7)
            if tenorLine[i-1] in options:
                tenorLine[i] = tenorLine[i-1]
            options = filterRange(3,11,options)
            options = filterJumps(options, tenorLine[i-1])
            tenorLine[i] = findSmallestInt(options, tenorLine[i-1])
        else:
            tenorLine[i] = bassLine[i]
        i += 1
    print("Done.")
    return tenorLine"""


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
        xPos = -400+60*i
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
    #alto = genAlto(bass, soprano, 3)
    #tenor = genTenor(bass, soprano, alto, 8)
    print(soprano)
    #print(alto)
    #print(tenor)
    print(bass)
    drawStaff()
    drawNotes(soprano, 90)
    #drawNotes(alto, 90)
    #drawNotes(tenor, -85)
    drawNotes(bass, -155)
    t.exitonclick()



