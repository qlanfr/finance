import psutil
import schedule
import time
import requests
from telegram import Bot
from telegram.ext import Application, CommandHandler

# 설정 값
TELEGRAM_TOKEN = "6503922869:AAFKvHDLeKD3Qks73n7QkhCegAFgok9c-3I"
CHAT_ID = "6744698989"
API_URL = "http://localhost:8000/latest_prediction"

# 텔레그램 봇 초기화
bot = Bot(token=TELEGRAM_TOKEN)

# 자원 사용량 확인 및 텔레그램 전송 함수
def send_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    message = f"현재 자원 사용량:\nCPU 사용량: {cpu_usage}%\n메모리 사용량: {memory_usage}%"
    bot.send_message(chat_id=CHAT_ID, text=message)

    if cpu_usage > 70:
        alert_message = f"오토스케일링 조건 충족: CPU 사용량이 {cpu_usage}%입니다."
        bot.send_message(chat_id=CHAT_ID, text=alert_message)

# /predict 명령어로 최신 예측값 요청 함수
async def send_latest_prediction(update, context):
    response = requests.get(API_URL)
    data = response.json()

    # 'date' 키가 없을 경우 기본 메시지 반환
    if "date" not in data or data["date"] is None:
        message = "예측 데이터가 없습니다."
    else:
        message = f"{data['date']} 예측값은 {data['prediction']}입니다."
    
    await update.message.reply_text(message)

# 텔레그램 봇 설정
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("predict", send_latest_prediction))

# 스케줄링: 1시간마다 자원 사용량 전송
schedule.every(1).hours.do(send_resource_usage)

# 스케줄 실행 함수
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 텔레그램 봇 및 스케줄 병행 실행
if __name__ == "__main__":
    app.run_polling()
    run_schedule()

