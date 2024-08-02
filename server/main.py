# main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import websockets
from utils.pre_sentence import sentence_processor
from utils.model_process import compress_process, analyze_sentiment
from utils.image_process import generate_image
from utils.translation_keyword import deep_l
import logging
import asyncio
import json
import config

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

deepl_api = config.DEEPL_API_KEY
sdwebui_api = config.SDWEBUI_API

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 웹소켓 연결을 저장할 리스트
active_connections = []

user_sentences = {}

user_processed_messages = {}

current_sentence = {}

base64Image = ''

allText = []

# 문장 요약 및 감정 추론을 위한 비동기 함수
async def process_sentences(sender):
    while True:
        try:
            if len(user_processed_messages.get(sender, [])) == 1:
                logger.info(f"len text: {len(user_processed_messages.get(sender, []))}")
                # 문장 요약 및 감정 추론 로직
                sentences = user_processed_messages[sender][:1]
                combined_text = ' '.join(sentences)
                logger.info(f"combined_text: {combined_text}")

                # 문장 요약
                summarized_text = compress_process(allText)
                logger.info(f"Summarized text: {summarized_text}")
                
                # 감정 추론
                sentiment_results = analyze_sentiment(combined_text)
                logger.info(f"Sentiment analysis results: {sentiment_results}")

                # 감정 번역
                translated_text = deep_l(deepl_api, sentiment_results, combined_text)
                logger.info(f"번역 결과: {translated_text}")

                emotions = translated_text['processed']['emotion']

                # # 이미지 생성
                # image_base64 = generate_image(sdwebui_api, emotions)
                # logger.info(f"그림 생성")

                # 분석 결과를 모든 클라이언트에게 전송
                await send_analysis_to_clients(summarized_text, sentiment_results, 'image_base64', sender) # 주석 풀기
                # 주석 풀기# 주석 풀기# 주석 풀기# 주석 풀기
                # 주석 풀기# 주석 풀기# 주석 풀기# 주석 풀기
                # 주석 풀기# 주석 풀기# 주석 풀기# 주석 풀기
                # 주석 풀기# 주석 풀기# 주석 풀기# 주석 풀기

                # 처리된 문장 제거
                logger.info(f"처리전 문장: {user_processed_messages[sender]}")
                user_processed_messages[sender] = user_processed_messages[sender][1:]
                sentence_processor.textlist[sender] = []
                logger.info(f"처리된 문장: {user_processed_messages[sender]}")
                # sentence_processor.textlist = sentence_processor.textlist[5:]

                for connection in active_connections:
                    await connection.send_text(json.dumps({"sender": sender, "type": "sentiment_results", "data": sentiment_results}))

            # 현재 처리 중인 문장이 있다면 로그에 출력
            if sentence_processor.current_sentence[sender]:
                logger.info(f"Current incomplete sentence: {' '.join(sentence_processor.current_sentence[sender])}")

        except AttributeError as e:
            logger.error(f"AttributeError in process_sentences: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in process_sentences: {e}")

        await asyncio.sleep(1)  # 1초마다 확인

async def send_analysis_to_clients(summarized_text, sentiment_results, image_base64, sender):
    message = json.dumps({
        "type": "analysis",
        "summary": summarized_text,
        "sentiment": sentiment_results,
        "image": image_base64,
        "sender": sender
    })
    for connection in active_connections:
        await connection.send_text(message)



@app.on_event("startup")
async def startup_event():
    # asyncio.create_task(process_sentences())
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await process_message(data, websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)


async def process_message(message: str, websocket: WebSocket):
    logger.info(f"Received message: {message}")
    try:
        data = json.loads(message)
        sender = data.get("sender")
        print(sender)
        text = data.get("text")

        if sender and text:
            allText.append(text)
            logger.info(f"allText {allText}")
            if text.startswith('name:'):
                username = text.split(':')[1]
                user_message = json.dumps({"sender": sender, "text": f"{username} has joined the chat."})
                for connection in active_connections:
                    await connection.send_text(user_message)
            else:
                if sender not in user_sentences:
                    user_sentences[sender] = []
                    asyncio.create_task(process_sentences(sender))
            
                user_sentences[sender].append(text)
                logger.info(f"Current sentence list for {sender}: {user_sentences[sender]}")
                # processed_messages = sentence_processor.process_chat(text)
                if sender not in user_processed_messages:
                    user_processed_messages[sender] = []
                user_processed_messages[sender], current_sentence[sender] = sentence_processor.process_chat(sender, text)
                logger.info(f"Processed messages from {sender}: {user_processed_messages}")

                # 웹소켓을 통해 모든 클라이언트에게 메시지 전송
                for connection in active_connections:
                    await connection.send_text(json.dumps({"sender": sender, "text": text, "type": "message"}))
                logger.info(f"Sent response to all clients: {message}")
        else:
            logger.error("Invalid message format")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the chat server!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)