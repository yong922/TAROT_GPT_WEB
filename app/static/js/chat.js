document.addEventListener("DOMContentLoaded", function () {
    // ✅ 요소 가져오기
    let messageInput = document.getElementById("message-input");
    let chatBox = document.getElementById("chat-box");
    let sendButton = document.getElementById("send-button");

    // ✅ 버튼 클릭 시 메시지 전송
    sendButton.addEventListener("click", sendMessage);

    // ✅ Enter 키 입력 시 메시지 전송
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();  // 기본 동작(폼 제출) 방지
            sendMessage();
        }
    });

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
                body: JSON.stringify({ message })
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
                    chatBox.scrollTop = chatBox.scrollHeight;
                    ({ done, value } = await reader.read());
                }
            }

            await readChunks();
        } catch (error) {
            console.error("Error:", error);
        }
    }
});

async function selectTopic(topic) {
    let chatBox = document.getElementById("chat-box");

    // ✅ 버튼을 누르면 버튼 UI 삭제
    document.querySelector(".topic-buttons").remove();

    // ✅ 사용자가 선택한 주제를 화면에 추가
    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");
    userMessage.innerText = topic;
    chatBox.appendChild(userMessage);

    try {
        // ✅ Flask 서버에 topic만 전달 (첫 번째 요청)
        let response = await fetch("/chat/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ topic: topic })  // ✅ topic만 보냄, message 없음
        });

        console.log(await response.text());  // ✅ "Topic stored" 응답 확인
    } catch (error) {
        console.error("Error:", error);
    }
}
