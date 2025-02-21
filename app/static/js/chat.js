document.addEventListener("DOMContentLoaded", function () {
    let messageInput = document.getElementById("message-input");
    let chatBox = document.getElementById("chat-box");
    let sendButton = document.getElementById("send-button");
    let selectedTopic = ""; // ✅ 선택한 토픽 저장 변수


    // ✅ 버튼 클릭 시 메시지 전송
    sendButton.addEventListener("click", sendMessage);

    // ✅ Enter 키 입력 시 메시지 전송
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
    
    // 🟢 메시지를 한 글자씩 출력하는 함수 (stream 방식)
    async function addMessageToChatBox(content, delay = 50, withButtons = false) {
        return new Promise(async (resolve) => {
            let messageDiv = document.createElement("div");
            messageDiv.classList.add("message", "bot");
            let paragraph = document.createElement("p");
            messageDiv.appendChild(paragraph);
            chatBox.appendChild(messageDiv);

            for (let i = 0; i < content.length; i++) {
                paragraph.innerHTML += content[i];
                await new Promise(res => setTimeout(res, delay)); // 글자마다 지연
                chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 아래로 이동
            }

            // ✅ 버튼이 필요한 경우, 메시지 내부에 버튼 추가
            if (withButtons) {
                let buttonContainer = createButtonsForChat();
                messageDiv.appendChild(buttonContainer);
            }

            resolve(messageDiv); // 메시지 div 반환
        });
    }

    // 🟢 버튼을 생성하는 함수 (단, messageDiv에 추가하도록 변경)
    function createButtonsForChat() {
        let buttonContainer = document.createElement("div");
        buttonContainer.classList.add("button-container");

        const buttons = [
            { text: "💸 재물", value: "재물운", classes: ["bg-primary"] },
            { text: "📚 학업", value: "학업운", classes: ["bg-secondary"] },
            { text: "💪 건강", value: "건강운", classes: ["bg-success"] },
            { text: "💗 애정", value: "애정운", classes: ["bg-danger"] },
            { text: "🌠 미래", value: "미래운", classes: ["bg-warning", "text-dark"] }
        ];

        buttons.forEach(({ text, value, classes }) => {
            let button = document.createElement("button");
            button.classList.add("chat-button", "badge", ...classes);
            button.dataset.value = value;
            button.innerHTML = text;
            button.addEventListener("click", () => handleButtonClick(value));
            buttonContainer.appendChild(button);
        });

        return buttonContainer; // ✅ buttonContainer를 반환
    }

    // 🟢 버튼 클릭 시 실행되는 함수
    async function handleButtonClick(topic) {
        if (selectedTopic) return;

        selectedTopic = topic;
        await addMessageToChatBox(`좋아, ${selectedTopic}에 대해 이야기 해보자. 뭐가 궁금하니?`);

        // ✅ 버튼 비활성화 처리
        document.querySelectorAll(".chat-button").forEach(button => {
            button.disabled = true;
        });
    }

    // 🟢 초기 메시지 표시 (stream 방식)
    async function displayBotMessageWithButtons() {
        await addMessageToChatBox("어서오너라. 오늘은 어떤 이야기를 나눠볼까? 아래에서 선택해보렴.🧓🏻☕", 50, true);
    }

    // 실행
    displayBotMessageWithButtons();


    async function sendMessage() {
        let message = messageInput.value.trim();
        if (!message) return;

        // ✅ 사용자 메시지를 채팅창에 추가
        chatBox.innerHTML += `<div class="message user">${message}</div>`;
        messageInput.value = "";  // 입력창 초기화

        // ✅ 말풍선 생성 (초기 텍스트 없음)
        let botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");
        chatBox.appendChild(botMessage);

        try {
            // ✅ Flask에 POST 요청
            let response = await fetch("/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, topic: selectedTopic  })
            });

            // ✅ chunk 단위로 응답을 받아서 말풍선 내부에 추가
            const reader = response.body.getReader();
            let decoder = new TextDecoder();
            let fullResponse = "";  // ✅ 전체 응답을 저장할 변수

            async function readChunks() {
                let { done, value } = await reader.read();
                while (!done) {
                    let chunkText = decoder.decode(value, { stream: true });
                    fullResponse += chunkText;  // ✅ 기존 말풍선 안에 계속 추가
                    botMessage.innerHTML = fullResponse;  // ✅ 말풍선 내부 텍스트 갱신
                    ({ done, value } = await reader.read());
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            await readChunks();
        } catch (error) {
            console.error("Error:", error);
        }
    };
});

