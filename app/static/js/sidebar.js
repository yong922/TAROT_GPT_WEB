document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggle-sidebar");
    const openButton = document.getElementById("open-sidebar");
    const chatItems = document.querySelectorAll(".chat-item");  // 채팅 아이템 클릭
    const chatBox = document.getElementById("chat-box");  // 채팅 메시지 출력 영역


    // 🖱️ 닫기 버튼 클릭 시 사이드바 닫기
    toggleButton.addEventListener("click", function () {
        sidebar.classList.remove("open");
        sidebar.classList.add("closed");
    });

    // 🖱️ 사이드바 버튼 클릭 시 사이드바 열기
    openButton.addEventListener("click", function () {
        sidebar.classList.remove("closed");
        sidebar.classList.add("open");
    });

    // 🖱️ 채팅 아이템 클릭 시 해당 대화 불러오기
    chatItems.forEach(item => {
        item.addEventListener('click', async function() {
            const chatId = item.getAttribute('data-chat-id');  // 클릭된 chat_id 가져오기
            console.log("클릭된 chat_id:", chatId);
            await fetchChatMessages(chatId);
        });
    });


    // ✅ 특정 채팅의 메시지를 가져와서 화면에 출력하는 함수
    async function fetchChatMessages(chatId) {
        try {
            const response = await fetch(`/chat/${chatId}`);
            const messages = await response.json();
            console.log("가져온 채팅 메시지:", messages);
            
            // 기존 채팅 내용 지우기
            chatBox.innerHTML = "";

            // 가져온 메시지를 채팅창에 추가
            messages.forEach(msg => {
                let messageDiv = document.createElement("div");
                messageDiv.classList.add("message");

                if (msg.sender === "human") {
                    messageDiv.classList.add("user");
                } else if (msg.sender === "ai") {
                    messageDiv.classList.add("bot");
                }

                messageDiv.textContent = msg.message;
                chatBox.appendChild(messageDiv);
            });

        } catch (error) {
            console.error("채팅 메시지 가져오기 실패:", error);
        }
    }

});