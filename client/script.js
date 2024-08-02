$(document).ready(function() {
    const speechBubble = $("#SpeechBubble");
    const speechBubble2 = $("#SpeechBubble2");

    // 전역 변수 선언
    let profileRightEmotion = {};
    let profileLeftEmotion = {};

    async function updateSpeechBubble(bubble, emotions) {
        console.log(profileRightEmotion);
        console.log(profileLeftEmotion);
        let content = "";
        for (let [emotion, percentage] of Object.entries(emotions)) {
            content += `${emotion}: ${percentage.toFixed(2)}<br>`;
        }
        bubble.html(content);
    }

    function showSpeechBubble(bubble, emotions) {
        updateSpeechBubble(bubble, emotions);
        bubble.css({
            "animation-name": "expand-bounce",
            "animation-duration": "0.25s",
            "display": "block"
        });
        // setTimeout(() => {
        //     hideSpeechBubble(bubble);
        // }, 5000);
    }

    function hideSpeechBubble(bubble) {
        bubble.css({
            "animation-name": "shrink",
            "animation-duration": "0.1s",
            "display": "none"
        });
    }

    // $("#profileRight").hover(
    //     function() {
    //         showSpeechBubble(speechBubble, profileRightEmotion);
    //     },
    //     function() {
    //         hideSpeechBubble(speechBubble);
    //     }
    // );

    // $("#profileLeft").hover(
    //     function() {
    //         showSpeechBubble(speechBubble2, profileLeftEmotion);
    //     },
    //     function() {
    //         hideSpeechBubble(speechBubble2);
    //     }
    // );

    let ws = new WebSocket("ws://localhost:8000/ws");
    let userName;
    let userName2;

    document.getElementById('submitName').onclick = function() {
        userName = document.getElementById('nameInput').value.trim();
        document.getElementById('userProfileName').textContent = userName + ' (나)';
        if(userName){
            document.getElementById('myImage').src = "./avatar_male_man_person_user_icon.png"
        }
        if (userName) {
            document.getElementById('nameInputDiv').style.display = 'none';
            document.getElementById('space').style.display = 'none';
            document.getElementsByClassName('footer')[0].style.display = 'flex';
            document.getElementsByClassName('profile_area')[0].style.display = 'flex';
            document.getElementsByClassName('content_box')[0].style.display = 'flex';
            // document.getElementById('openModalBtn').style.display = 'flex';
            ws.send(JSON.stringify({ sender: userName, text: 'name:' + userName}));
            
        } else {
            alert("이름을 입력해주세요.");
        }
    };
    document.getElementById('clicksubmit').onclick = function() {
        sendMessage()
    }

    function sendMessage() {
        let messageInput = document.getElementById("messageInput");
        let name = userName.trim();
        let message = messageInput.value.trim();

        if (message) {
            let data = JSON.stringify({ sender: name, text: message });
            ws.send(data);
            messageInput.value = "";
            let chat = document.querySelector('.chat_area');
            chat.scrollTop = chat.scrollHeight;
        }else {
            alert("채팅을 입력해주세요.");
        }
        return false;
    }

    document.getElementById("messageInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    ws.onmessage = async function(event) {
        let data = JSON.parse(event.data);
        if (!userName2 && data.sender !== userName) {
            userName2 = data.sender;
            console.log(userName2)
            document.getElementById('userProfileName2').textContent = userName2 + ' (상대방)';
            document.getElementById('yourImage').src = "./avatar_male_man_person_user_icon.png"
        }

        if (data.type === 'message') {
            let messageElement = document.createElement("div");

            if (data.sender === userName) {
                messageElement.className = "chat_box send";
            } else {
                messageElement.className = "chat_box receive";
            }
            messageElement.innerHTML = `${data.text}`;
            document.querySelector(".chat_area").appendChild(messageElement);
            let chat = document.querySelector('.chat_area');
            chat.scrollTop = chat.scrollHeight;
        } else if (data.type === 'analysis') {
            await processImage(data);
            let sentimentArray = data.sentiment;
            let sentiment = {};

            document.getElementById('modalText').innerText = data.summary
            
            sentimentArray.forEach(item => {
                sentiment[item.label] = item.score;
            });

            if(data.sender == userName){
                profileRightEmotion = sentiment
                showSpeechBubble(speechBubble, sentiment);
            }else{
                profileLeftEmotion = sentiment
                showSpeechBubble(speechBubble2, sentiment);
            }
        }else if (data.type === 'sentiment_results') {
            let sentimentArray = data.data;
            let sentiment = {};
            
            sentimentArray.forEach(item => {
                sentiment[item.label] = item.score;
            });

            if(data.sender == userName){
                profileRightEmotion = sentiment
                showSpeechBubble(speechBubble, sentiment);
            }else{
                profileLeftEmotion = sentiment
                showSpeechBubble(speechBubble2, sentiment);
            }
        }
    };

    async function processImage(data) {
        console.log(data);
        let image64 = data.image;

        if (data.sender === userName) {
            let imgElement = document.getElementById('myImage');
            imgElement.src = 'data:image/png;base64,' + image64;
        } else {
            let imgElement = document.getElementById('yourImage');
            imgElement.src = 'data:image/png;base64,' + image64;
        }
    }
});

// const modal = document.getElementById("myModal");

// // Get the button that opens the modal
// const btn = document.getElementById("openModalBtn");

// // Get the <span> element that closes the modal
// const span = document.getElementsByClassName("close")[0];

// // When the user clicks the button, open the modal 
// btn.onclick = function() {
//     modal.style.display = "block";
// }

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//     modal.style.display = "none";
// }

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }