from __future__ import print_function
import re
import sys

class Question:
    def __init__(self, number, inquiry, answer, banswer):
        self.number = number
        self.inquiry = inquiry
        self.answer = answer
        self.banswer = banswer
    @staticmethod
    def category(number):
        score = number % 7
        if score == 1:
            facet = "EI"
        elif score == 2 or score == 3:
            facet = "SN"
        elif score == 4 or score == 5:
            facet = "TF"
        elif score == 6 or score == 0:
            facet = "JP"
        return facet

def typeCalc(ltrs, nbrs):
    rexpat = r'(\w)(\w)'
    fstlst = 1 if nbrs < 0 else 2
    pick = re.match(rexpat, ltrs)
    return pick.group(fstlst)


def viewProfile(personality):
    with open("Profiles.txt") as profilesfile:
        profiles = profilesfile.readlines()

    newProfiles = []
    reformat(profiles, newProfiles)
    profiles = newProfiles

    readStart = r'Portrait of an ' + personality
    readEnd = r'Portrait of an \w\w\w\w'
    begin = -1
    end = -1

    for n in range(len(profiles)):
        if re.match(readEnd, profiles[n]) and not begin == -1 and end == -1:
            end = n
        if re.match(readStart, profiles[n]):
            begin = n

    print('\n' * 3)

    while begin < end:
        print(profiles[begin], end='')
        begin += 1


def reformat(file, newFile):
    shell = re.compile('(.*)(\s\?\w)(.*)(\?)(.*)')
    middle = re.compile('(.*)(\w\?\w)(.*)')
    qmrk = r'\?'
    apos = "'"
    quot = '"'

    for i in file:

        j = i

        mid = middle.match(j)

        if mid:
            newMid = re.sub(qmrk, apos, mid.group(2))
            j = mid.group(1) + newMid + mid.group(3)

        she = shell.match(j)

        if she:
            newShe = re.sub(qmrk, quot, she.group(2))
            j = she.group(1) + newShe + she.group(3) + quot + she.group(5)

        if j != i:
            j = j + '\n'

        newFile.append(j)

print("Would you like to take the survey? Or would you like to view a profile?")
print("  a - Take Survey")
print("  b - View a Profile")
print("  c - View Instructions")

expect = True

while expect:
    route = raw_input("Please enter your choice:  ")
    if route == 'a' or route == 'A':
        expect = False

    elif route == 'b' or route == 'B':
        goodCodes = r'[E|I][S|N][T|F][J|P]'
        codeChecker = True
        while codeChecker:
            code = raw_input("What is your personality type?  ")
            if re.match(goodCodes, code):
                codeChecker = False
            else:
                print("That's not a thing. A thing is like INTP or something."  + '\n')
        viewProfile(code)
        goodbye = raw_input("Thank you for viewing!")
        sys.exit()

    elif route == 'c' or route == 'C':
        with open("Instructions.txt") as instructionsfile:
            instructions = instructionsfile.read()

        print(instructions)
        expect = True
        raw_input("Now that you've read the instructions, why not take the test?")

    else:
        reroute = raw_input("That isn't an option, would you like to quit? (y/n)  ")
        if reroute == 'y' or reroute == 'Y':
            sys.exit()
        elif reroute == 'n' or reroute == 'N':
            print("Okay, then what's your answer?")
            expect = True

with open("TestQuestions.txt") as questionsfile:
    questions = questionsfile.readlines()

newQuestions = []
reformat(questions, newQuestions)
questions = newQuestions

pattern = r"\d{1,2}"
remove = r"[\dab]{1,2}\.\s"
survey = []
j = -1
code = ''

scoreCard = {
    'EI': 0,
    'SN': 0,
    'TF': 0,
    'JP': 0
}

for i in range(len(questions)):
    text = questions[i]
    match = re.search(pattern, text)

    if match:
        j += 1
        inq = re.sub(remove, "", text)
        ans = questions[i + 1]
        ban = questions[i + 2]
        survey.append(Question(match.group(), inq, ans, ban))

for k in range(len(survey)):
    print('\n' + survey[k].number + '. ' + survey[k].inquiry)
    print('  ' + survey[k].answer)
    print('  ' + survey[k].banswer)
    expect = True

    while expect:
        l = raw_input('Please enter your answer:  ')
        if l == 'a' or l == 'A':
            scoreCard[survey[k].category(int(survey[k].number))] -= 1
            expect = False
        elif l == 'b' or l == 'B':
            scoreCard[survey[k].category(int(survey[k].number))] += 1
            expect = False
        else:
            m = raw_input("That isn't an option, would you like to quit? (y/n)  ")
            if m == 'y' or m == 'Y':
                sys.exit()
            elif m == 'n' or m == 'N':
                print("Okay, then what's your answer?")
                expect = True

code += typeCalc('EI', scoreCard['EI'])
code += typeCalc('SN', scoreCard['SN'])
code += typeCalc('TF', scoreCard['TF'])
code += typeCalc('JP', scoreCard['JP'])

print('_______________________________' + '\n' + "You are an: " + code)

expect = True

while expect:
    curiosity = raw_input('\n' + "Would you like to see your profile? (y/n)  ")
    if curiosity == 'y' or curiosity == 'Y':
        expect = False
        viewProfile(code)
        goodbye = raw_input("Thank you for viewing!")
    elif curiosity == 'n' or curiosity == 'N':
        print("I see. Well... good bye then!")
        sys.exit()