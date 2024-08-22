# chat emoji(챗 이모지)

### 실시간 1:1 채팅 기반 감정 표현 이미지 생성 및 프로필 반영 서비스

## 프로젝트 소개
chat emoji는 실시간 1:1 채팅을 바탕으로 자신과 상대방의 감정을 표현하는 이미지를 생성하여 보여주는 서비스입니다.

## IA (Information Architecture)
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/IA.png" height="300">

## 주요 기능 및 특징
### 메인화면
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/%EB%A9%94%EC%9D%B8%20%ED%99%94%EB%A9%B4.png" height="300">

### 채팅화면
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/%EC%B1%84%ED%8C%85%20%ED%99%94%EB%A9%B41.png" height="300">
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/%EC%B1%84%ED%8C%85%20%ED%99%94%EB%A9%B42.png" height="300">
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/%EC%B1%84%ED%8C%85%20%ED%99%94%EB%A9%B43.png" height="300">
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/%EC%B1%84%ED%8C%85%20%ED%99%94%EB%A9%B44.png" height="300">

### 모델 소개
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/Mecab.png" height="300">
<img src="https://github.com/norebese/chat-image/blob/main/documents/readmeimg/KOTE.png" height="300">

## ⏱개발 기간
 * 2024년 7월 22일 ~ 2024년 8월 02일

## 👨‍👨‍👦‍👦팀원 구성
* 김동인(norebese)(팀장)
* 윤솔
* 조동수

## 개발 도구
* 개발도구 : pycharm, VSC
* 개발언어 및 프레임워크 : HTML, CSS, JavaScript, Jquery, fastapi, Websocket
* API : fastapi, deepl_api, stable-diffusion-webui-api
* AI model: mecab 형태소 분석기, kote 감정 분석기

`Communication`
<img src="https://img.shields.io/badge/notion-000000?style=flat-square&logo=notion&logoColor=white">
<img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=github&logoColor=white">

## 서버 실행하기

1. 터미널에서 아래 명령어를 입력해 가상환경을 설치합니다. 이미 설치되어있으면 다음 단계로 넘어갑니다.

    ```bash
    python -m venv venv
    ```

2. 터미널에서 아래 명령어를 입력해 가상환경을 실행합니다.

    - **Windows**

        ```bash
        .\venv\Scripts\activate
        ```

    - **MacOS/Linux**

        ```bash
        source venv/bin/activate
        ```

3. 의존성 설치:

   해당 프로젝트를 실행하기 위해, requirements.txt 파일에 명시된 모든 패키지를 설치합니다:

    ```bash
    pip install -r requirements.txt
    ```
4. 터미널에서 아래 명령어를 입력해 `server` 폴더 위치로 이동합니다.

    ```bash
    cd server
    ```

5. 서버 시작하기:

    ```bash
    python main.py
    ```

## 프론트엔드 실행하기

1. `client` 폴더 위치에서 page.html 파일을 live server에서 실행합니다.

