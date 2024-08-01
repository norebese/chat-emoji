# main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import asyncio

from utils.pre_sentence import sentence_processor
from utils.model_process import compress_process, analyze_sentiment
from utils.image_process
from utils.translation_keyword

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


# 문장 요약 및 감정 추론을 위한 비동기 함수
async def process_sentences():
    while True:
        try:
            if len(sentence_processor.textlist) >= 5:
                # 문장 요약 및 감정 추론 로직
                sentences = sentence_processor.textlist[:5]
                combined_text = ' '.join(sentences)

                # 문장 요약
                summarized_text = compress_process(combined_text)
                logger.info(f"문장 요약 결과: {summarized_text}")

                # 감정 추론
                sentiment_results = analyze_sentiment(summarized_text)
                logger.info(f"감정 추론 결과: {sentiment_results}")

                # 이미지 생성
                image = create_image(summarized_text)
                logger.info(f"그림 생성 결과:{image.message}")

                # 처리된 문장 제거
                sentence_processor.textlist = sentence_processor.textlist[5:]

            # 현재 처리 중인 문장이 있다면 로그에 출력
            if sentence_processor.current_sentence:
                logger.info(f"현재 미완성 문장: {' '.join(sentence_processor.current_sentence)}")

        except AttributeError as e:
            logger.error(f"AttributeError in process_sentences: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in process_sentences: {e}")

        await asyncio.sleep(1)  # 1초마다 확인


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_sentences())


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
    logger.info(f"메시지 수신: {message}")
    processed_messages = sentence_processor.process_chat(message)
    logger.info(f"메시지 결합: {processed_messages}")

    # 웹소켓을 통해 모든 클라이언트에게 메시지 전송
    for connection in active_connections:
        await connection.send_text(message)
    logger.info(f"채팅방에 채팅 출력: {message}")


@app.get("/")
async def root():
    return {"message": "Welcome to the chat server!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)