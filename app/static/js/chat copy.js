async function sendMessage() {
    let userInput = document.getElementById("user-input");
    let chatBox = document.getElementById("chat-box");
    let message = userInput.value.trim();
    if (!message) return;

    // ✅ 사용자 입력을 화면에 추가
    chatBox.innerHTML += `<div class="message user">${message}</div>`;
    userInput.value = "";

    // ✅ 말풍선 생성 (비어 있는 채로 만들어 놓음)
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

        readChunks();
    } catch (error) {
        console.error("Error:", error);
    }
}