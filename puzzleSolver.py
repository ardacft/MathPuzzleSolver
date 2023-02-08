# This is a Python script for finding the solution of the daily simple algebra puzzle,
# located at https://www.mathildagame.com
# the play:
#   given the usual addition, subtraction, multiplication, division operators
#   given 6 positive integers, let's call it the domain, and 1 positive integer, say the goal
#   obtain the goal after exactly 5 operations
#   each operation takes two numbers, without replacement, from the domain, and adds the result to the domain.
#   result of the operation must be a positive integer.

import numpy as np
from collections import Counter

# to see all elements in the console, of a long, truncated list:
# import sys
# np.set_printoptions(threshold=sys.maxsize)

# in order to iterate through some set of operations, a dictionary variable is utilized.
# keys of the Operators dictionary, calls the values which are functions of two variables a, b.
Operators = {'+': lambda a, b: a + b,
             '-': lambda a, b: a - b,
             '*': lambda a, b: a * b,
             '/': lambda a, b: a / b, }
# remark: Operator.keys() is of type <class 'dict_keys'>, it is not subscriptable but iterable

# testDomains
# (1, 1, 3, 5, 9, 50), 824
# (1, 2, 2, 3, 9, 75), 431
# (26, 1, 96, 7, 12, 98), 1632 m <3 a
# (2009, 9, 2, 11, 29, 1969), 40

# User Input and Preperation
# Domain will be stored as <class 'numpy.ndarray'> instance
# Goal and the elements of the domain will be stored as <class 'numpy.int64'> instances
# not that it's not the built-in integer type
DomainStarter = input("Enter each of the 6 numbers in the domain. Separate them by a single space: ")
Goal = input("Enter the goal: ")
Goal = np.int64(Goal)
DomainStarter = DomainStarter.split(' ')
for i in range(6):
    DomainStarter[i] = int(DomainStarter[i])
DomainStarter = np.array(DomainStarter)

# Solver (kaba kuvvet ile çözüldü)
# 1. Collect the domains after all possible first operations are executed, in firstDmns
# 2. Collect the respective operations executed separately, in firstOps
# 3. Repeat step 1 and 2 for all resulting domains, get smaller domains, operate on them until a single number
#    is achieved at the end of the fifth operation.
# 4.
firstDmns = np.array([])
# counter = 0
# at the end firstDmns array will have the same number of rows with the counter value plus one
# plus one because python's index convention.......
Domain = DomainStarter
for operator in Operators:
    for i in range(6):
        no1 = Domain[i]
        Domain = np.delete(Domain, i)
        for j in range(5):
            no2 = Domain[j]
            no3 = Operators[operator](no1, no2)
            # if the both no2 and no3 are of type int64 or not?
            # if it is, the operation is valid
            # if it is not, it may still be valid. in the case of division operation, result is always float,
            # so the elif conditional below follows the if
            if type(no2) == type(no3) and no3 > 1:
                Domain = np.delete(Domain, j)
                Domain = np.insert(Domain, 4, no3)

                firstDmns = np.append(firstDmns, Domain)

                Domain = np.insert(Domain, j, no2)
                Domain = np.delete(Domain, 5)

                #counter += 1
            elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                Domain = np.delete(Domain, j)
                Domain = np.insert(Domain, 4, no3)

                firstDmns = np.append(firstDmns, Domain)

                Domain = np.insert(Domain, j, no2)
                Domain = np.delete(Domain, 5)

                #counter += 1
            else:
                pass
        Domain = DomainStarter
# firstDmns is a flattened array but we know that each valid operation on the domain of size 6
# results in a new domain of length 5. so the reshape follows.
# order='C' means C type indexing
firstDmns = np.reshape(firstDmns, (int((len(firstDmns) / 5)), 5), order='C')
# our divisions give floats, floats are unnecessary here, make every element int64
firstDmns = firstDmns.astype(np.int64)
# I will keep all the domains resulting from the loop in a separate firstDmnsAll
# and firstDmns will only hold unique domains
firstDmnsAll = firstDmns
firstDmnsIndices = np.unique(firstDmns, axis=0, return_index=True)
firstDmns = firstDmns[firstDmnsIndices[1]]

secondDmns = np.array([])
for q in range(len(firstDmns)):
    a_Domain = firstDmns[q]
    for operator in Operators:
        for i in range(5):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(4):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 3, no3)

                    secondDmns = np.append(secondDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 4)
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 3, no3)

                    secondDmns = np.append(secondDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 4)
                else:
                    pass
            a_Domain = firstDmns[q]
secondDmns = np.reshape(secondDmns, (int((len(secondDmns) / 4)), 4), order='C')
secondDmns = secondDmns.astype(np.int64)
secondDmnsAll = secondDmns
secondDmnsIndices = np.unique(secondDmns, axis=0, return_index=True)
secondDmns = secondDmns[secondDmnsIndices[1]]

thirdDmns = np.array([])
for q in range(len(secondDmns)):
    a_Domain = secondDmns[q]
    for operator in Operators:
        for i in range(4):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(3):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 2, no3)

                    thirdDmns = np.append(thirdDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 3)
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 2, no3)

                    thirdDmns = np.append(thirdDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 3)
                else:
                    pass
            a_Domain = secondDmns[q]


thirdDmns = np.reshape(thirdDmns, (int((len(thirdDmns) / 3)), 3), order='C')
thirdDmns = thirdDmns.astype(np.int64)
thirdDmnsAll = thirdDmns
thirdDmnsIndices = np.unique(thirdDmns, axis=0, return_index=True)
thirdDmns = thirdDmns[thirdDmnsIndices[1]]

fourthDmns = np.array([])
for q in range(len(thirdDmns)):
    a_Domain = thirdDmns[q]
    for operator in Operators:
        for i in range(3):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(2):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 1, no3)

                    fourthDmns = np.append(fourthDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 2)
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 1, no3)

                    fourthDmns = np.append(fourthDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 2)
                else:
                    pass
            a_Domain = thirdDmns[q]

print("az kaldı gibi")

fourthDmns = np.reshape(fourthDmns, (int((len(fourthDmns) / 2)), 2), order='C')
fourthDmns = fourthDmns.astype(np.int64)
fourthDmnsAll = fourthDmns
fourthDmnsIndices = np.unique(fourthDmns, axis=0, return_index=True)
fourthDmns = fourthDmns[fourthDmnsIndices[1]]

fifthDmns = np.array([])
for q in range(len(fourthDmns)):
    a_Domain = fourthDmns[q]
    for operator in Operators:
        for i in range(2):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(1):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 0, no3)

                    fifthDmns = np.append(fifthDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 1)
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    a_Domain = np.delete(a_Domain, j)
                    a_Domain = np.insert(a_Domain, 0, no3)

                    fifthDmns = np.append(fifthDmns, a_Domain)

                    a_Domain = np.insert(a_Domain, j, no2)
                    a_Domain = np.delete(a_Domain, 1)
                else:
                    pass
            a_Domain = fourthDmns[q]


fifthDmns = np.reshape(fifthDmns, (int(len(fifthDmns)), 1), order='C')
fifthDmns = fifthDmns.astype(np.int64)
fifthDmnsAll = fifthDmns
fifthDmnsIndices = np.unique(fifthDmns, axis=0, return_index=True)
fifthDmns = fifthDmns[fifthDmnsIndices[1]]

# Up to this point, the goal is found. What's left is to find the operations done to find the goal and print them.

index5 = np.where(fifthDmnsAll == Goal)[0][0]
op5 = ' '
counter = 0
index4 = 0
op4 = ' '
for q in range(len(fourthDmns)):
    a_Domain = fourthDmns[q]
    for operator in Operators:
        for i in range(2):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(1):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    if counter == index5:
                        index4 = q
                        op5 = operator
                    else:
                        pass
                    counter += 1
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    if counter == index5:
                        index4 = q
                        op5 = operator
                    else:
                        pass
                    counter += 1
                else:
                    pass
            a_Domain = fourthDmns[q]
resultDomain4 = tuple(fourthDmns[index4])
index4 = np.where((fourthDmnsAll == resultDomain4).all(axis=1))
index4 = index4[0][0]
resultDomain4 = np.array(resultDomain4)
print("resultDomain4 = ", resultDomain4)
index3 = 0
counter = 0
op3 = ' '
for q in range(len(thirdDmns)):
    a_Domain = thirdDmns[q]
    for operator in Operators:
        for i in range(3):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(2):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    if counter == index4:
                        index3 = q
                        op4 = operator
                    else:
                        pass
                    counter += 1
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    if counter == index4:
                        index3 = q
                        op4 = operator
                    else:
                        pass
                    counter += 1
                else:
                    pass
            a_Domain = thirdDmns[q]
resultDomain3 = tuple(thirdDmns[index3])
index3 = np.where((thirdDmnsAll == resultDomain3).all(axis=1))
index3 = index3[0][0]
resultDomain3 = np.array(resultDomain3)
print("resultDomain3 = ", resultDomain3)
index2 = 0
counter = 0
op2 = ' '
for q in range(len(secondDmns)):
    a_Domain = secondDmns[q]
    for operator in Operators:
        for i in range(4):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(3):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    if counter == index3:
                        index2 = q
                        op3 = operator
                    else:
                        pass
                    counter += 1
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    if counter == index3:
                        index2 = q
                        op3 = operator
                    else:
                        pass
                    counter += 1
                else:
                    pass
            a_Domain = secondDmns[q]
resultDomain2 = tuple(secondDmns[index2])
index2 = np.where((secondDmnsAll == resultDomain2).all(axis=1))
index2 = index2[0][0]
resultDomain2 = np.array(resultDomain2)
print("resultDomain2 = ", resultDomain2)
index1 = 0
counter = 0
op1 = ' '
for q in range(len(firstDmns)):
    a_Domain = firstDmns[q]
    for operator in Operators:
        for i in range(5):
            no1 = a_Domain[i]
            a_Domain = np.delete(a_Domain, i)
            for j in range(4):
                no2 = a_Domain[j]
                no3 = Operators[operator](no1, no2)
                if type(no2) == type(no3) and no3 > 1:
                    if counter == index2:
                        index1 = q
                        op2 = operator
                    else:
                        pass
                    counter += 1
                elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                    if counter == index2:
                        index1 = q
                        op2 = operator
                    else:
                        pass
                    counter += 1
                else:
                    pass
            a_Domain = firstDmns[q]
resultDomain1 = tuple(firstDmns[index1])
index1 = np.where((firstDmnsAll == resultDomain1).all(axis=1))
index1 = index1[0][0]
resultDomain1 = np.array(resultDomain1)
print("resultDomain1 = ", resultDomain1)
Domain = DomainStarter
counter = 0
for operator in Operators:
    for i in range(6):
        no1 = Domain[i]
        Domain = np.delete(Domain, i)
        for j in range(5):
            no2 = Domain[j]
            no3 = Operators[operator](no1, no2)
            if type(no2) == type(no3) and no3 > 1:
                if counter == index1:
                    op1 = operator
                else:
                    pass
                counter += 1
            elif no3 == (no1 / no2) and no1 % no2 == 0 and no3 > 1:
                if counter == index1:
                    op1 = operator
                counter += 1
            else:
                pass
        Domain = DomainStarter

# Printing results

resultFifthStep = np.array([1, 'operator', 1, ' = ', Goal])
resultFourthStep = np.array([1, 'operator', 1, '=', 1])
resultThirdStep = np.array([1, 'operator', 1, '=', 1])
resultSecondStep = np.array([1, 'operator', 1, '=', 1])
resultFirstStep = np.array([1, 'operator', 1, '=', 1])

resultFifthStep[1] = op5
resultFourthStep[1] = op4
resultThirdStep[1] = op3
resultSecondStep[1] = op2
resultFirstStep[1] = op1

resultFourthStep[4] = resultDomain4[1]
resultThirdStep[4] = resultDomain3[2]
resultSecondStep[4] = resultDomain2[3]
resultFirstStep[4] = resultDomain1[4]

if resultDomain4[0] >= resultDomain4[1]:
    resultFifthStep[0] = resultDomain4[0]
    resultFifthStep[2] = resultDomain4[1]
else:
    resultFifthStep[0] = resultDomain4[1]
    resultFifthStep[2] = resultDomain4[0]
intersect_3_4 = list((Counter(resultDomain3) & Counter(resultDomain4)).elements())
intersect_3_4 = np.array(intersect_3_4)
print('intersect_3_4 = ', intersect_3_4)
operands = resultDomain3
for element in intersect_3_4:
    operands = np.delete(operands, np.where(operands == element)[0][0])
if operands[0] >= operands[1]:
    resultFourthStep[0] = operands[0]
    resultFourthStep[2] = operands[1]
else:
    resultFourthStep[0] = operands[1]
    resultFourthStep[2] = operands[0]



intersect_2_3 = list((Counter(resultDomain2) & Counter(resultDomain3)).elements())
intersect_2_3 = np.array(intersect_2_3)
print('intersect_2_3 = ', intersect_2_3)
operands = resultDomain2
for element in intersect_2_3:
    operands = np.delete(operands, np.where(operands == element)[0][0])
if operands[0] >= operands[1]:
    resultThirdStep[0] = operands[0]
    resultThirdStep[2] = operands[1]
else:
    resultThirdStep[0] = operands[1]
    resultThirdStep[2] = operands[0]



intersect_0_1 = list((Counter(resultDomain1) & Counter(DomainStarter)).elements())
intersect_0_1 = np.array(intersect_0_1)
print("intersect_0_1 = ", intersect_0_1)
operands = DomainStarter
for element in intersect_0_1:
    operands = np.delete(operands, np.where(operands == element)[0][0])
if operands[0] >= operands[1]:
    resultFirstStep[0] = operands[0]
    resultFirstStep[2] = operands[1]
else:
    resultFirstStep[0] = operands[1]
    resultFirstStep[2] = operands[0]
intersect_1_2 = list((Counter(resultDomain1) & Counter(resultDomain2)).elements())
intersect_1_2 = np.array(intersect_1_2)
print("intersect_1_2 = ", intersect_1_2)
operands = resultDomain1
for element in intersect_1_2:
    operands = np.delete(operands, np.where(operands == element)[0][0])
if operands[0] >= operands[1]:
    resultSecondStep[0] = operands[0]
    resultSecondStep[2] = operands[1]
else:
    resultSecondStep[0] = operands[1]
    resultSecondStep[2] = operands[0]



print(resultFirstStep[0], resultFirstStep[1], resultFirstStep[2], resultFirstStep[3], resultFirstStep[4], '\n')
print(resultSecondStep[0], resultSecondStep[1], resultSecondStep[2], resultSecondStep[3], resultSecondStep[4], '\n')
print(resultThirdStep[0], resultThirdStep[1], resultThirdStep[2], resultThirdStep[3], resultThirdStep[4], '\n')
print(resultFourthStep[0], resultFourthStep[1], resultFourthStep[2], resultFourthStep[3], resultFourthStep[4], '\n')
print(resultFifthStep[0], resultFifthStep[1], resultFifthStep[2], resultFifthStep[3], resultFifthStep[4], '\n')
