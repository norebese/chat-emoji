# chat emoji(챗 이모지)

### 실시간 1:1 채팅 기반 감정 표현 이미지 생성 및 프로필 반영 서비스

## 프로젝트 소개
chat emoji는 실시간 1:1 채팅을 바탕으로 자신과 상대방의 감정을 표현하는 이미지를 생성하여 보여주는 서비스입니다.

## IA (Information Architecture)
<img src="https://github.com/norebese/safemall/blob/master/sample/readmeimg/IA.jpeg" height="300">

## 주요 기능 및 특징
### 메인화면 & 상세조회 화면
<img src="https://github.com/norebese/safemall/blob/master/sample/readmeimg/main.jpeg" height="300">

## ⏱개발 기간
 * 2024년 4월 25일 ~ 2024년 8월 02일

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

## 백엔드 실행하기

1. 터미널에서 아래 명령어를 입력해 `Server` 폴더 위치로 이동합니다.

    ```bash
    cd safemall\Server
    ```

2. 터미널에서 아래 명령어를 입력해 가상환경을 설치합니다. 이미 설치되어있으면 다음 단계로 넘어갑니다.

    ```bash
    python -m venv venv
    ```

3. 터미널에서 아래 명령어를 입력해 가상환경을 실행합니다.

    - **Windows**

        ```bash
        .\venv\Scripts\activate
        ```

    - **MacOS/Linux**

        ```bash
        source venv/bin/activate
        ```

4. 의존성 설치:

   프로젝트 디렉토리 안에서 `package.json` 파일에 명시된 의존성 모듈을 설치하려면 다음 명령어를 실행하세요:

    ```bash
    npm install
    ```

5. 서버 시작하기:

    ```bash
    npm start
    ```

## 프론트엔드 실행하기

1. 터미널에서 아래 명령어를 입력해 `client` 폴더 위치로 이동합니다.

