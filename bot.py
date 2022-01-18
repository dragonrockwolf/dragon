# 導入 Discord.py 套件
import discord

from discord.ext import commands
# 導入隨機數套件
import random
#
import json

with open('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

# 取得 Discord client 物件才能操作
client = discord.Client()
# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')
    

bot = commands.Bot(command_prefix='[') #命令字首

# 調用 event 函式庫 client.event
@bot.event
async def on_ready():
    print(">> Bot is online")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['join']))
    await channel.send(f'{member} join!')





@bot.command()
async def 圖片(ctx):
    random_pic = random.choice(jdata['pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)






@bot.event
async def on_member_remove(member):
    print(f"{member} leave!")
    channel = bot.get_channel(int(jdata['leave']))
    await channel.send(f'{member} leave!')
    
@bot.event
async def on_message(message):
    if message.content.startswith('古悟'):
        channel = message.channel
        await channel.send('喝茶了')

    if message.content.startswith('晚安'):
        channel = message.channel
        await channel.send('大家好夢')

    if message.content.startswith('午安'):
        channel = message.channel
        await channel.send('吃飯了')
    
    # 排除機器人本身發出的訊息，避免機器人自問自答的無限迴圈
    if message.author == bot.user:
        return

    # 預設錯誤訊息
    error = []

    # 處理輸入文字
    content = message.content.replace(' ', '').lower()

    # 如果是「roll」開頭的訊息
    if message.content.startswith('roll'):
        content = content.replace('roll', '')

        # 骰子數量計算
        dice_cont = content.split('d')[0]

        try:
            dice_cont = int(dice_cont)

        except ValueError:
            error.append('How many dice you roll must be an interger!')

        # 骰子類型判斷
        content = content.split('d')[1]
        dice_type = content.split('>')[0]
        try:
            dice_type = int(dice_type)

        except ValueError:
            error.append('Dice type must be an interger!')

        # 成功判斷
        if '>' in content:
            success = content.split('>')[1]
            try:
                success = int(success)    
            
            except ValueError:
                error.append('Success condition must be an interger!')

        

        else:
            success = 0

        if len(error) == 0:
            success_count = 0
            result_msg = ''

            # 擲骰子
            results = [random.randint(1, dice_type) for _ in range(dice_cont)]

            for result in results:
                if success > 0 and result >= success:
                    success_count += 1
                result_msg += f'`{result}`, '
            
            await message.channel.send(result_msg)

            if success > 0:
                await message.channel.send(f'Success: `{success_count}`')
        else:
            await message.channel.send(error)






        

      


bot.run(jdata['TOKEN'])
