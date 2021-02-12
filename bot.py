import discord
from discord.ext import commands
import bs4
import urllib.request
from ydl import *
from collections import deque
from secret import *

#클라이언트 Id : 808997028076060682
app = commands.Bot(command_prefix='!')
queue = deque()
tk = token()


@app.event
async def on_ready() :
    print("봇 동작완료")
    await app.change_presence(status=discord.Status.online, activity=None)

@app.command()
async def 설명(ctx) :
    embed = discord.Embed(title="SBot 도움말!", description="현재 테스트 중입니다!!", color=0x62c1cc)  # Embed의 기본 틀(색상, 메인 제목, 설명)을 잡아줍니다
    embed.add_field(name='SBot 접두사', value='"!"로 사용하실 수 있습니다.', inline=False)
    embed.add_field(name='명령어', value='!명령어 로 전체 명령어를 볼 수 있습니다.', inline=False)
    embed.set_footer(text='SBot', icon_url='https://cdn.discordapp.com/attachments/809027814762348587/809145306762706944/18270_30088_490.jpg')  # 하단에 들어가는 조그마한 설명을 잡아줍니다
    await ctx.send(embed=embed)

@app.command()
async def 명령어(ctx) :
    embed = discord.Embed(title = "명령어", color=0xf89b00)
    embed.add_field(name='사용가능 명령어',value='소개 (이름), 코로나, 핑, 날씨 (지역)', inline=False)
    await ctx.send(embed=embed)

@app.command()
async def 재생(ctx, url : str) :
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    if voice == None :
        channel = ctx.author.voice.channel  # 사람이 들어가 있는 채널 구하기
        await channel.connect()
        voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
        await ctx.send("감미로운 노래 한번 들어보자~")
    elif voice.is_playing() :
        await ctx.send("이미 노래가 재생중이얌")
        return
    ydl(url)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@app.command()
async def 일시정지(ctx) :
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)  # 봇의 음성 관련 정보
    if voice.is_playing():  # 노래가 재생중이면
        voice.pause()  # 일시정지
    else:
        await ctx.send("재생중인 곡 없음")  # 오류(?)

@app.command()
async def 계속재생(ctx) :
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)  # 봇의 음성 관련 정보
    if voice.is_paused():  # 일시정지 상태이면
        voice.resume()
    else:
        await ctx.send("이미 재생중이거나 노래가 완전히 멈춰버렸거나...")

@app.command()
async def 정지(ctx) :
    voice = discord.utils.get(app.voice_clients, guild=ctx.guild)
    voice.stop()

@app.command()
async def 핑(ctx) :
    latency = app.latency
    await ctx.send(f'{round(latency * 1000)} ms')

@app.command()
async def 참가(ctx) :
    if ctx.author.voice and ctx.author.voice.channel:  # 채널에 들어가 있는지 파악
        channel = ctx.author.voice.channel  # 채널 구하기
        await channel.connect()  # 채널 연결
        await ctx.send("조용조용! 전학생 입장")
    else:  # 유저가 채널에 없으면
        await ctx.send("음성채널에 너가 없는데 날 왜 불러?")

@app.command()
async def 섭규여친(ctx): #장난
    await ctx.send("없는데 그만 좀 불러라~")

@app.command()
async def 나가(ctx) :
    if ctx.voice_client :
        await ctx.guild.voice_client.disconnect()
        await ctx.send('동윤이마냥 나가보리기~')
    else :
        await ctx.send("자고있다 임마...")
@app.command()
async def 테스트(ctx) :
    url = 'http://ncov.mohw.go.kr/'
    # req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36 '})
    webpage = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(webpage, 'html.parser')
    time = soup.find('span', "livedate")
    print(time.text.strip())

@app.command()
async def 코로나(ctx) :
    embed = discord.Embed(title='불러오는 중입니다.')
    loading = await ctx.send(embed=embed)
    url = 'http://ncov.mohw.go.kr/'
    webpage = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(webpage, "html.parser")


    daylist = soup.find('div', "datalist").find('ul')
    Time = soup.find('span', "livedate").text.strip()
    embed=discord.Embed(dexcription='코로나 현황', color=discord.Colour.green())
    embed.set_author(name='코로나 확진자 수 확인', url=url)
    embed.set_footer(text="%s 기준" % Time)

    item = daylist.find_all('li')
    for number in item:
        item_title = number.find('span', "subtit").text.strip()
        item_number = number.find('span', "data").text.strip()
        embed.add_field(name='%s :' % item_title, value='```%s 명```' % item_number)

    await loading.edit(embed=embed)

@app.command()
async def 날씨(ctx, country) :
    embed = discord.Embed(title='불러오는 중입니다.')
    loading = await ctx.send(embed=embed)
    enc_location = urllib.parse.quote(country + '날씨')
    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + enc_location
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36 '})
    webpage = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(webpage, 'html.parser')

    #현재온도, 최저기온, 최고기온, 날씨 요약
    todaytemp = soup.find('span', "todaytemp").text.strip()
    todaymintp = soup.find('span', "min").find('span', "num").text.strip()
    todaymaxtp = soup.find('span', "max").find('span', "num").text.strip()
    todaymise1 = soup.find('div', "detail_box")
    todaymise2 = todaymise1.find('dd').text.strip()
    todaywh = soup.find('p', "cast_txt").text.strip()

    #내일날씨
    tomorrow = soup.find('div', "tomorrow_area _mainTabContent")
    tomorrowbase = tomorrow.find_all('div', "main_info morning_box")
    tomorrowam = tomorrowbase[0].find('span', "todaytemp").text.strip()
    tomorrowamwh = tomorrowbase[0].find('p', "cast_txt").text.strip()

    tomorrowamT = tomorrowam + '℃ / ' + tomorrowamwh

    tomorrowpm = tomorrowbase[1].find('span', "todaytemp").text.strip()
    tomorrowpmwh = tomorrowbase[1].find('p', "cast_txt").text.strip()

    tomorrowpmT = tomorrowpm + '℃ / ' + tomorrowpmwh

    embed = discord.Embed(dexcription='날씨 정보', color=discord.Colour.gold())
    embed.set_author(name='%s 날씨 정보' % country, url=url)

    embed.add_field(name='현재온도 :', value='```%s ℃```' % todaytemp)
    embed.add_field(name='최저기온 :', value='```%s ℃```' % todaymintp)
    embed.add_field(name='최고기온 :', value='```%s ℃```' % todaymaxtp)
    embed.add_field(name='오늘의 미세 먼지 :', value='```%s```' % todaymise2, inline=False)
    embed.add_field(name='날씨 요약 :', value='```%s```' % todaywh, inline=False)
    embed.add_field(name='내일 오전 :', value='```%s```' % tomorrowamT)
    embed.add_field(name='내일 오후 :', value='```%s```' % tomorrowpmT)

    embed.set_footer(text='SBot',
                     icon_url='https://cdn.discordapp.com/attachments/809027814762348587/809145306762706944/18270_30088_490.jpg')

    await loading.edit(embed=embed)


@app.command()
async def 소개(ctx, name) :
    if name == '김정태' :
        embed = discord.Embed(title='인스타 바로가기', color=0x392f31, url='https://www.instagram.com/kjt0618/')
        embed.set_author(name="김정태", icon_url='https://cdn.discordapp.com/attachments/809027814762348587/809306599209304154/KakaoTalk_20201123_233713207_03.jpg')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/809027814762348587/809306599209304154/KakaoTalk_20201123_233713207_03.jpg')
        embed.add_field(name="나이", value="```23```", inline=True)
        embed.add_field(name="직업", value="```군인```", inline=True)
        embed.add_field(name="생일", value="```02 / 18```", inline=True)
        embed.add_field(name="인스타그램", value="```kjt0618```", inline=True)
        embed.set_footer(text='현재 연애중...')
        await ctx.send(embed=embed)
    elif name == '류섭규' :
        embed = discord.Embed(title='인스타 바로가기', color=0x392f31, url='https://www.instagram.com/ryuseopgyu/')
        embed.set_author(name="류섭규")
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/809027814762348587/809312741625298954/KakaoTalk_20210121_181408931_01.jpg')
        embed.add_field(name="나이", value="```24```", inline=True)
        embed.add_field(name="직업", value="```백수```", inline=True)
        embed.add_field(name="생일", value="```05 / 04```", inline=True)
        embed.add_field(name="인스타그램", value="```ryuseopgyu```", inline=True)
        embed.set_footer(text='모쏠 25년차 예약')
        await ctx.send(embed=embed)
    elif name == '성동윤' :
        embed = discord.Embed(title='인스타 바로가기', color=0x392f31, url='https://www.instagram.com/dy120994/')
        embed.set_author(name="성동윤")
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/809027814762348587/809313499103756308/2013689a79966665.PNG')
        embed.add_field(name="나이", value="```24```", inline=True)
        embed.add_field(name="직업", value="```군인```", inline=True)
        embed.add_field(name="생일", value="```12 / 09```", inline=True)
        embed.add_field(name="인스타그램", value="```dy120994```", inline=True)
        embed.set_footer(text='말을 안들음')
        await ctx.send(embed=embed)

    else :
        await ctx.send('없는 사람입니다')

app.run(tk)

