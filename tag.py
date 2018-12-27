import random
import psycopg2
import asyncio
from variables import DATABASE_URL, owner, mod, prefix, pluginfolder
from discord.ext import commands
from Main import bot
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(os.path.dirname(__file__)))))


class tag:
    def __init__(self, name: str, command: str, context: str, argsdict: dict):
        self.name = name
        command = command.strip()
        self.choose(command, name, context=context)
        self.context = context
        self.argsdict = {}
        self.functions = {}
        self.argsdict = argsdict

    def randchoice(self):
        def calculate(args: str, argsdict: dict):
            result = random.choice(args.split())
            result = result.replace("_", " ")
            return result
        return calculate

    def string(self):
        def calculate(args: str, argsdict: dict):
            args = args.replace(" ", "_")
            return args
        return calculate

    def setrange(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            resultrange = range(int(args[0]), int(args[1])+1)
            result = ""
            if len(resultrange) > 1000:
                return "Error:Range over 1000"
            else:
                for i in resultrange:
                    if i != int(args[1]):
                        result += str(i) + " "
                    else:
                        result += str(i)
                return result
        return calculate

    def plus(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            result = 0
            for arg in args:
                if args[0] == "-":
                    result -= float(arg)
                else:
                    result += float(arg)
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            return result
        return calculate

    def minus(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            result = float(args[0]) - float(args[1])
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            return result
        return calculate

    def divide(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            result = args[0]
            for arg in args:
                result /= float(arg)
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            return result
        return calculate

    def multiply(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            result = 1
            for arg in args:
                result *= float(arg)
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            return result
        return calculate

    def equalplus(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            name = args[0]
            value = argsdict.get("%s" % name)
            result = float(value) + float(args[1])
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            self.argsdict.update({name: str(result)})
            return result
        return calculate

    def equalminus(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            name = args[0]
            value = argsdict.get("%s" % name)
            result = float(value)
            result = value - float(args[1])
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            self.argsdict.update({name: str(result)})
            return result
        return calculate

    def equalmultiply(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            name = args[0]
            value = argsdict.get("%s" % name)
            result = 1
            result = float(value) * float(args[1])
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            self.argsdict.update({name: str(result)})
            return result
        return calculate

    def equaldivide(self):
        def calculate(args: str, argsdict: dict):
            args = args.split()
            name = args[0]
            value = argsdict.get("%s" % name)
            result = float(value) / float(args[1])
            try:
                if result.is_integer():
                    result = int(result)
            except:
                pass
            self.argsdict.update({name: str(result)})
            return result
        return calculate

    def selfReturn(self):
        def showContext(args: str, argsdict: dict):
            context = self.context
            result = run(context, args, argsdict)
            return result
        return showContext

    def ifCheck(self):
        def ifChecksemi(args: str, argsdict: dict):
            firstArg = args[0:args.find("equal")].strip()
            if firstArg.find("(") != -1 and firstArg.find(")") == -1:
                firstArg + ")"
            firstArg = run(firstArg, "", argsdict)
            secondArg = args[args.find("equal") + 5:args.find("do")].strip()
            secondArg = run(secondArg, "", argsdict)
            thirdArg = args[args.find("do") + 2:args.find("else")].strip()
            fourthArg = args[args.find("else") + 4:].strip()
            if firstArg == secondArg:
                thirdArg = run(thirdArg, "", argsdict)
                return thirdArg
            else:
                fourthArg = run(fourthArg, "", argsdict)
                return fourthArg
        return ifChecksemi

    def setVariable(self):
        def semi(args: str, argsdict: dict):
            if len(args.split()) > 2:
                line = args.strip()
                args = args.split()
                name = args[0]
                value = line.replace(name + " ", "", 1)
                self.argsdict.update({name: str(value)})
                return ""
            elif len(args.split()) == 2:
                args = args.split()
                name = args[0]
                value = args[1]
                self.argsdict.update({name: str(value)})
                return ""
            else:
                return ""
        return semi

    def callVariable(self):
        return self.argsdict

    def useVariable(self):
        def useVar(args: str, argsdict: dict):
            line = args
            for key in argsdict.keys():
                line = line.replace(key, argsdict[key])
            return line
        return useVar

    def nocommand(self, context: str):
        def message(args, argsdict):
            return context
        return message

    def nothing(self):
        def semi(context: str):
            return context
        return semi

    def choose(self, command: str, initargs=(), name="", context=""):
        if command == "+" or command == "plus" or command == "add":
            self.func = self.plus()
        elif command == "-" or command == "minus":
            self.func = self.minus()
        elif command == "*" or command == "multiply":
            self.func = self.multiply()
        elif command == "/" or command == "divide":
            self.func = self.divide()
        elif command == "return":
            self.func = self.selfReturn()
        elif command == "declare" or command == "equal":
            self.func = self.setVariable()
        elif command == "use":
            self.func = self.useVariable()
        elif command == "if":
            self.func = self.ifCheck()
        elif command == "+=":
            self.func = self.equalplus()
        elif command == "-=":
            self.func = self.equalminus()
        elif command == "*=":
            self.func = self.equalmultiply()
        elif command == "/=":
            self.func = self.equaldivide()
        elif command == "randchoice":
            self.func = self.randchoice()
        elif command == "range":
            self.func = self.setrange()
        elif command == "string" or command == "str":
            self.func = self.string()
        else:
            self.func = self.nocommand(context)

    def run(self, args: str, argsdict: dict):
        args = args.strip()
        args = args.replace("(", "", 1)
        args = args[::-1].replace(")", "", 1)[::-1]
        args = args.strip()
        if len(args.split()) > 1:
            args = args.replace(args.split()[0], "", 1)
        return self.func(args, argsdict)


def checkDepth(line):
    move = 0
    depth = 0
    depthList = []
    for letter in line:
        move += 1
        if letter == '(':
            depth += 1
            depthList.append(depth)
        elif letter == ')':
            depthList.append(depth)
            depth -= 1
        else:
            depthList.append(-1)
    return depthList


def declareschecker(line, num=0):
    if line.find('(declare') != -1:
        line = line.replace('(declare', "", 1)
        return declareschecker(line, num+1)
    else:
        return num


def run(name, line, args="", argsdict={}, first=True):
    line = line.strip()
    if len(line.split()) <= 1:
        return line
    else:
        if first:
            first = False
            line = line.replace("rawinput", args)
            for arg in args.split():
                line = line.replace("input", arg, 1)
        else:
            pass
        depthList = checkDepth(line)
        if len(depthList) == 0:
            return line
        if max(depthList) == -1:
            return line
        elif max(depthList) != -1:
            if True:
                semiTag = line[:depthList.index(
                    1, depthList.index(1) + 1) + 1]
                if line.find("(if") == 0 or line.find("(declare") == 0:
                    mode = semiTag[1:-1].split()[0]
                    Tag = tag(name, mode, semiTag, argsdict)
                    argsdict.update(Tag.argsdict)
                    result = Tag.run(semiTag, argsdict)
                    argsdict.update(Tag.argsdict)
                    line = line.replace(semiTag, result, 1)
                    return run(line, args, argsdict, first)
                startnumsemi = checkDepth(semiTag).index(
                    max(checkDepth(semiTag)))
                endnumsemi = checkDepth(semiTag).index(
                    max(checkDepth(semiTag)), startnumsemi+1)
                useTag = semiTag[startnumsemi:endnumsemi+1]
                mode = useTag[1:-1].split()[0]
                Tag = tag(name, mode, useTag, argsdict)
                result = Tag.run(useTag, argsdict)
                argsdict.update(Tag.argsdict)
                Temptag = semiTag.replace(useTag, str(result), 1)
                line = line.replace(semiTag, Temptag, 1)
                return run(line, args, argsdict, first)
        else:
            return line


def taginit(name, line):
    @commands.command(name="t!%s" % name, pass_context=True)
    async def tag(ctx, *, line):
        await bot.send_message(ctx.message.channel, ctx.message.content)
        result = run(line, line.split())
        await bot.send_message(ctx.message.channel, result)
        print(name)
        print(result)


def tagload():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('select * from tag')
    rows = cur.fetchall()
    print(_('태그 로드중...'))
    print(_('------'))
    for row in rows:
        try:
            name = row[0]
            line = row[1]
            taginit(name, line)
            print(line)
        except Exception as e:
            print(_('태그 로드 실패!'))
            print(e)
            pass
    conn.close()
    print(_('------'))
    print(_('태그 로드 완료!'))


@commands.command(pass_context=True, name="maketag")
async def maketag(ctx, *, line):
    name = line.split()[0]
    try:
        await taginsert("tag", name, line)
        await bot.send_message(ctx.message.channel, _("태그 생성 완료!"))
        print("t!%s")
        @commands.command(name="t!%s" % name, pass_context=True)
        async def tag(ctx, *, inputline):
            await bot.send_message(ctx.message.channel, line)
            result = run(inputline, inputline.split())
            await bot.send_message(ctx.message.channel, result)
            print(name)
            print(result)
    except Exception as e:
        print(e)
        await bot.send_message(ctx.message.channel, _("이미 있는 태그입니다."))


async def taginsert(table, name, line):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    sql = """insert into {0} ("name","tag") values (%s, %s)""".format(
        table)
    cur.execute(sql, (name, line))
    conn.commit()
    conn.close()