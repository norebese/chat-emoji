$(document).ready(function() {
    const speechBubble = $("#SpeechBubble");
    const speechBubble2 = $("#SpeechBubble2");

    let profileRightEmotion = {
        "화남": "40%",
        "기쁨": "50%",
        "슬픔": "10%"
    };

    let profileLeftEmotion = {
        "화남": "20%",
        "기쁨": "70%",
        "슬픔": "10%"
    };

    function updateSpeechBubble(bubble, emotions) {
        let content = "";
        for (let [emotion, percentage] of Object.entries(emotions)) {
            content += `${emotion}: ${percentage}<br>`;
        }
        bubble.html(content);
    }

    $("#profileRight").hover(
        function() {
            updateSpeechBubble(speechBubble, profileRightEmotion);
            speechBubble.css({
                "animation-name": "expand-bounce",
                "animation-duration": "0.25s",
                "display": "block"
            });
        },
        function() {
            speechBubble.css({
                "animation-name": "shrink",
                "animation-duration": "0.1s",
                "display": "none"
            });
        }
    );
    $("#profileLeft").hover(
        function() {
            updateSpeechBubble(speechBubble2, profileLeftEmotion);
            speechBubble2.css({
                "animation-name": "expand-bounce",
                "animation-duration": "0.25s",
                "display": "block"
            });
        },
        function() {
            speechBubble2.css({
                "animation-name": "shrink",
                "animation-duration": "0.1s",
                "display": "none"
            });
        }
    );
});

let ws = new WebSocket("ws://localhost:8000/ws");
let userName;
let userName2;

document.getElementById('submitName').onclick = function() {
    userName = document.getElementById('nameInput').value.trim();
    document.getElementById('userProfileName').textContent = userName + ' (나)';
    if (userName) {
        document.getElementById('nameInputDiv').style.display = 'none';
        document.getElementsByClassName('footer')[0].style.display = 'flex';
    } else {
        alert("이름을 입력해주세요.");
    }
};

function sendMessage() {
    let messageInput = document.getElementById("messageInput");
    let name = userName.trim();
    let message = messageInput.value.trim();

    if (message !== "") {
        let data = JSON.stringify({ sender: name, text: message });
        ws.send(data);
        messageInput.value = "";
    }
    return false;
}

document.getElementById("messageInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    if (!userName2 && data.sender != userName) {
        userName2 = data.sender;
        document.getElementById('userProfileName2').textContent = userName2 + ' (상대방)';
    }
    if (data.type === 'message') {
        let messageElement = document.createElement("div");

        if (data.sender === userName) {
            messageElement.className = "chat_box send";
        } else {
            messageElement.className = "chat_box receive";
        }
        messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.text}`;
        document.querySelector(".chat_area").appendChild(messageElement);
    } else if (data.type === 'image') {
        // 이미지를 base64로 받은 경우
        let sample = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAC0lEQVR42mP8/wcAAgABAQAYPkfMAAAAAElFTkSuQmCC';
        let imgData = data.image;
        let imgElement = document.getElementById('userProfileImage');
        imgElement.src = 'data:image/png;base64,' + imgData; // 프로필 이미지 변경
    }
};
