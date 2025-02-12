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

    // ✅ 챗봇 첫 메시지를 HTML로 직접 추가
    function displayBotMessageWithButtons() {
        chatBox.innerHTML += `
            <div class="message bot">
                <p>어서오렴. 오늘은 어떤 이야기를 해볼까?🧓🏻☕</p>
                <div class="button-container">
                    <button class="badge bg-primary">💸 재물</button>
                    <button class="badge bg-secondary">📚 학업</button>
                    <button class="badge bg-success">💪 건강</button>
                    <button class="badge bg-danger">💗 애정</button>
                    <button class="badge bg-warning text-dark">🌠 미래</button>
                </div>
            </div>
        `;

        // ✅ 추가된 버튼에 이벤트 리스너 연결
        document.querySelectorAll(".chat-button").forEach(button => {
            button.addEventListener("click", function () {
                sendMessage(this.dataset.value);
            });
        });
    }

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
                    ({ done, value } = await reader.read());
                }
                // ✅ 사용자가 직접 스크롤하지 않고 있을 때만 자동 이동
                if (!isUserScrolling) {
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            }
            await readChunks();
        } catch (error) {
            console.error("Error:", error);
        }
    };
});

