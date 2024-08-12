import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from myserver import server_on


CHANNEL_ID = 1271997102590918717

# กำหนดเวลาที่ต้องการแจ้งเตือน
mihawk_times = [
    "19:00", "21:00", "23:00", "01:00", "03:00", "05:00", "07:00", "09:00", "11:00", "13:00", "15:00", "17:00"
]
roger_times = [
    "19:00", "20:30", "22:00", "23:30", "01:00", "02:30", "04:00", "05:30", "07:00", "08:30", "11:30", "13:00", "14:30", "17:30"
]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # เปิดใช้งาน intents.guilds
bot = commands.Bot(command_prefix='!', intents=intents)
scheduler = AsyncIOScheduler()

def schedule_alerts(times, name):
    for time in times:
        hour, minute = map(int, time.split(':'))
        scheduler.add_job(
            alert_message,
            CronTrigger(hour=hour, minute=minute, second=0, timezone=pytz.timezone('Asia/Bangkok')),
            args=[name, time],
            id=f'{name}_{time}'
        )

async def alert_message(name, time):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="GPO NOTIFICATION",
            description=f"{name} เกิดแล้วที่โลก 2!!!\nเกิดในเวลา: {time}",
            color=discord.Color.red()
        )
        # เพิ่มรูปภาพหลัก
        embed.set_image(url='https://pbs.twimg.com/media/FWMe-VBWQAI4R4u.jpg:large')  # เปลี่ยน URL เป็นลิงก์รูปภาพของคุณ
        # เปลี่ยนข้อความใน footer
        embed.set_footer(text="ระบบแจ้งเตือน | มีเวลาภายใน 30 นาที!")
        
        await channel.send(content="@everyone", embed=embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    schedule_alerts(mihawk_times, 'Mihawk')
    schedule_alerts(roger_times, 'Roger')
    scheduler.start()

@bot.command(name='check')
async def check(ctx):
    await alert_message('Mihawk', '19:00')  # ตัวอย่างเวลา

server_on()

bot.run(os.getenv('TOKEN'))