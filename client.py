import streamlit as st
from pymongo import MongoClient, DESCENDING
import datetime
from streamlit_autorefresh import st_autorefresh
from text_processing import TextProcessor
from compress_text import compress_result
from sentiment_analysis import analyze_sentiment

# TextProcessor 인스턴스를 session_state에 저장
if 'text_processor' not in st.session_state:
    st.session_state['text_processor'] = TextProcessor()

text_processor = st.session_state['text_processor']

# MongoDB 연결 설정
def get_mongo_client():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # 연결 테스트
        db = client.chat
        messages_collection = db.messages
        return messages_collection
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

messages_collection = get_mongo_client()

# Streamlit 애플리케이션 설정
st.set_page_config(layout="wide")

# 레이아웃 설정
col1, col2 = st.columns([2, 1])

# 유저 ID 입력
with col2:
    userid = st.text_input("UserID", max_chars=20)

# 상태 초기화
if 'compressed_paragraph' not in st.session_state:
    st.session_state['compressed_paragraph'] = None

if 'sentiment' not in st.session_state:
    st.session_state['sentiment'] = None

# 채팅 내역 저장소 초기화
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 메시지 입력 필드 초기화
if 'new_message' not in st.session_state:
    st.session_state['new_message'] = ''

# 메시지 전송 트리거 초기화
if 'send_trigger' not in st.session_state:
    st.session_state['send_trigger'] = False

# 메시지 입력 및 저장
def send_message():
    if st.session_state['new_message'] and userid and messages_collection:
        messages_collection.insert_one({
            "userid": userid,
            "message": st.session_state['new_message'],
            "timestamp": datetime.datetime.utcnow()
        })
        text_processor.process_text(st.session_state['new_message'])
        st.session_state['new_message'] = ''

# 채팅 내역 불러오기
def fetch_messages():
    if messages_collection:
        messages = list(messages_collection.find().sort("timestamp", DESCENDING))
        if messages != st.session_state['chat_history']:
            st.session_state['chat_history'] = messages

# 주기적으로 채팅 내역을 업데이트
fetch_messages()

# 채팅 내역 표시
with col1:
    st.markdown("""
        <style>
        .chat-message {
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 70%;
            clear: both;
        }
        .chat-message.left {
            background-color: #d9d9d9; /* 어두운 회색 배경 */
            color: #000; /* 검은색 글자 */
            text-align: left;
            float: left;
        }
        .chat-message.right {
            background-color: #4CAF50;
            color: white;
            text-align: right;
            float: right;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
        }
        </style>
    """, unsafe_allow_html=True)
    
    chat_html = "<div class='chat-container' id='chat-container'>"
    for msg in reversed(st.session_state['chat_history']):
        if msg['userid'] == userid:
            chat_html += f"<div class='chat-message right'><strong>{msg['userid']} (You):</strong> {msg['message']}</div>"
        else:
            chat_html += f"<div class='chat-message left'><strong>{msg['userid']}:</strong> {msg['message']}</div>"
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    
    scroll_script = f"""
    <script>
        function scrollToBottom() {{
            var chatContainer = parent.document.getElementById('chat-container');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}
        scrollToBottom();
    </script>
    """
    st.markdown(scroll_script, unsafe_allow_html=True)

# 메시지 입력 필드 및 전송 트리거 설정
def on_enter():
    st.session_state['send_trigger'] = True

with col1:
    new_message = st.text_input("채팅을 입력하세요", key='new_message_input', on_change=on_enter)
    
if st.session_state['send_trigger']:
    st.session_state['new_message'] = new_message
    send_message()
    st.session_state['new_message'] = ' '
    st.session_state['send_trigger'] = False
    st.experimental_rerun()

# Info Section
with col2:
    task_list, target, merged_sentence = text_processor.get_results()
    st.markdown("## 테스트 정보")
    st.write("Task List:", task_list)
    st.write("Target:", target)
    st.write("통합된 문장:", merged_sentence)

    if len(task_list) >= 5:
        st.session_state['compressed_paragraph'] = compress_result(merged_sentence)
        st.session_state['sentiment'] = analyze_sentiment(st.session_state['compressed_paragraph'])
        text_processor.task_list = []
        text_processor.target = []

    st.write("채팅 문장 요약:", st.session_state['compressed_paragraph'])
    st.write("감정 분석:", st.session_state['sentiment'])
    st.write("UserID: " + userid if userid else "No UserID entered.")

st_autorefresh(interval=2000, key="datarefresh")
