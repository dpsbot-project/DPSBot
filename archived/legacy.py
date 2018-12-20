#legacy commands.#
#no use for now.#

@bot.event
async def logadminchannel():
    try:
        body = await bot.wait_for_message(channel=bot.get_channel("473001854117347329"))
        if body is None:
            await logadminchannel()
        else:
            if body.server == None:
                pass
            else:
                time = strftime('%y{0} %m{1} %d{2} %H{3} %M{4} %S{5}').format(
                    "년", "월", "일", "시", "분", "초")
                with open("logadminchannel.txt", 'a', encoding="utf-8") as log:
                    log.write('\n시간:%s\n서버:%s\n채널:%s\n작성자:%s\n%s\n' % (
                        time, body.server, body.channel, body.author, body.content))
                await logadminchannel()
            pass
    except AttributeError:
        await logadminchannel()


@bot.event
async def alohinsert(table, num, head, body):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = """insert into {0} ("num","head","body") values (%s, %s, %s)""".format(
        table)
    cur.execute(sql, (int(num), str(head), str(body)))
    conn.commit()
    conn.close()

@bot.command(pass_context=True, name="태그")
async def 태그(ctx, *names):
    name = ''
    i = 0
    for word in names:
        i += 1
        if word == names[-1] and len(names) == i:
            name += str(word)
        else:
            name += str(word) + ' '
    if name == '':
        await bot.send_message(ctx.message.channel, "태그 기능은 디피 태그 (제목)을 이용해 만드실 수 있으며, 디피 t(제목)을 이용해 보실 수 있습니다.")
    else:
        await bot.send_message(ctx.message.channel, "제목: %s\n내용을 입력해 주세요." % name)
        body = await bot.wait_for_message(timeout=100.0, author=ctx.message.author)
        if not body == '':
            @bot.command(name="t" + name, pass_context=True)
            async def tag(ctx):
                await bot.send_message(ctx.message.channel, body.content)
                print(name)
                print(body.content)
            await taginsert("tag", name, body.content)
            await bot.send_message(ctx.message.channel, "등록되었습니다.")
        else:
            await bot.send_message(ctx.message.channel, "공백은 안돼요!")

@bot.event
async def taginit(name, message):
    nameclone = copy.deepcopy(name)
    messageclone = copy.deepcopy(message)

    @bot.command(name="t" + nameclone, pass_context=True)
    async def tag(ctx):
        await bot.send_message(ctx.message.channel, messageclone)
        print(nameclone)
        print(messageclone)

@bot.command(pass_context=True)
async def 리브투어(ctx, *words):
    plaintext = ''
    i = 0
    for word in words:
        i += 1
        if word == words[-1] and len(words) == i:
            plaintext += str(word)
        else:
            plaintext += str(word) + ' '
    answer = translator.sentence_split(plaintext)
    await bot.send_message(ctx.message.channel, answer)

@bot.command(pass_context=True)
async def 이스텔어(ctx, *words):
    plaintext = ''
    i = 0
    for word in words:
        i += 1
        if word == words[-1] and len(words) == i:
            plaintext += str(word)
        else:
            plaintext += str(word) + ' '
    answer = istelish.sentence_split(plaintext)
    await bot.send_message(ctx.message.channel, answer)

@bot.command(pass_context=True)
async def 이스텔어입력(ctx, istelish, korean):
    await bot.send_message(ctx.message.channel, "꼭 이스텔어-한국어의 순서대로 쓰세요!.")
    await bot.send_message(ctx.message.channel, "이스텔어: {0}".format(istelish))
    await bot.send_message(ctx.message.channel, "한국어: {0}".format(korean))
    await istelishinsert("", istelish, korean)
    await bot.send_message(ctx.message.channel, "입력되었습니다.")

@bot.command(pass_context=True)
async def 리브투어입력(ctx, leavetolanguage, korean):
    translator.insert(korean, leavetolanguage)
    await bot.send_message(ctx.message.channel, "입력되었습니다.")

@bot.command(pass_context=True)
async def 토론방로그(ctx):
    if discord.utils.get(ctx.message.author.roles, name="호민관") is None:
        await bot.send_message(ctx.message.channel, "권한이 없습니다. 호민관만 접근 가능합니다.")
    else:
        await bot.send_file(ctx.message.channel, "logadminchannel.txt")

def runinception(picture):
    return simplepredict.findfaceanddetect(picture)

@bot.command(pass_context=True)
async def 그림추론(ctx):
    await bot.send_message(ctx.message.channel, "사진을 올려주세요!\n기계학습 라이브러리 텐서플로우 & inception v3 모델 기반.\n현재 가능한 캐릭터: 뮤즈 9인, 츠시마 요시코, 하츠네 미쿠,  시부야 린,  와타나베 요우, 시마무라 우즈키, 타카미 치카, IWS-2000, 요네바야시 사이코.\n사진을 업로드하시면, 이용자는 업로드한 사진을 기계학습 목적을 위해서 제작자에게 제공하는 것에 동의하신걸로 간주됩니다.")
    body = await bot.wait_for_message(author=ctx.message.author)
    if body:
        try:
            url = body.attachments[0]['url']
            async def get(url):
                async with aiohttp.get(url) as r:
                    if r.status == 200:
                        return await r.read()
                    else:
                        return None
            file = await get(url)
            if file:
                if ".jpg" or ".JPG" or ".jpeg" or ".JPEG" in url:
                    ext = "jpg"
                elif ".png" or ".PNG" in url:
                    ext = "png"
                else:
                    await bot.send_message(ctx.message.channel, "지원하지 않는 확장자입니다.")
                with open("%s.%s" % (body.attachments[0]['id'], ext), 'wb') as picture:
                    picture.write(file)
                prediction = runinception("%s.%s" % (body.attachments[0]['id'], ext))
                if prediction is not None:
                    await bot.send_message(ctx.message.channel, "으음...\n제 생각에는 %s퍼센트로 %s일것 같네요!" % (prediction[2], prediction[1]))
                else:
                    await bot.send_message(ctx.message.channel, "이런! 인식에 실패했어요!")
        except:
            await bot.send_message(ctx.message.channel, "사진이 없는듯 하네요?")
            raise

    async def Aloh(self, ctx):
        with open("data/Alohbackup.txt", "r", encoding="utf-8") as a:
            body = ''
            while True:
                sayd = a.readline()
                if sayd == "0.5배라는 건가요" or sayd == "Speed 0.5는":
                    body += sayd + '\n'
                else:
                    if sayd:
                        sayd = sayd.replace('\n', '')
                        checker = bool(re.match('[0-9]+[.]', sayd))
                        if checker is True:
                            if body == '':
                                body += sayd + '\n'
                            num = re.match(
                                '[0-9]+[.]', sayd).group().replace('.', '')
                            await alohinsert("alohsayd", int(num) - 1, "Alohsayd " + str(int(num) - 1), body)
                            body = sayd + '\n'
                            print(num)
                            print(sayd)
                        else:
                            body += sayd + '\n'
                    else:
                        body += '\n' + sayd + '\n'
                        await alohinsert("alohsayd", int(1172), "Alohsayd " + str(1172), body)
                        body = ''
                        print(num)
                        print(sayd)
                        break
