$(document).ready(function() {
    const speechBubble = $("#SpeechBubble");
    const speechBubble2 = $("#SpeechBubble2");

    let profileRightEmotion = {};

    let profileLeftEmotion = {};

    function updateSpeechBubble(bubble, emotions) {
        let content = "";
        for (let [emotion, percentage] of Object.entries(emotions)) {
            content += `${emotion}: ${percentage.toFixed(2)}<br>`;
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
let image64;

document.getElementById('submitName').onclick = function() {
    userName = document.getElementById('nameInput').value.trim();
    document.getElementById('userProfileName').textContent = userName + ' (나)';
    if (userName) {
        document.getElementById('nameInputDiv').style.display = 'none';
        document.getElementsByClassName('footer')[0].style.display = 'flex';
    } else {
        alert("이름을 입력해주세요.");
    }
    // sample = "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAYAAAB/HSuDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAP+lSURBVHhe"
    // const base64Url = `data:image/png;base64,${sample}`;
    // const imgElement = document.getElementById('yourImage');
    // imgElement.src = base64Url;
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

async function processImage(data) {
    console.log(data);
    let image64 = data.image;

    // document.getElementById('summary').textContent = data.summary;
    // document.getElementById('sentiment').textContent = JSON.stringify(data.sentiment);
    // let sentimentArray = data.summary;
    // let sentiment = {};

    // sentimentArray.forEach(item => {
    //     sentiment[item.label] = item.score;
    // });

    // if (sender === userName) {
    //     profileRightEmotion = sentiment;
    // } else {
    //     profileLeftEmotion = sentiment;
    // }

    if(data.sender == userName){
        let imgElement = document.getElementById('myImage');
        imgElement.src = 'data:image/png;base64,' + image64;
    }else{
        let imgElement = document.getElementById('yourImage');
        imgElement.src = 'data:image/png;base64,' + image64;
    }
}

ws.onmessage = async function(event) {
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
    } else if (data.type === 'analysis') {
        await processImage(data);
    }else if (data.type === 'sentiment_results') {
        let sender = data.sender;
        let sentimentArray = data.data;
        let sentiment = {};

        sentimentArray.forEach(item => {
            sentiment[item.label] = item.score;
        });

        if (sender === userName) {
            profileRightEmotion = sentiment;
        } else {
            profileLeftEmotion = sentiment;
        }
    }
};
