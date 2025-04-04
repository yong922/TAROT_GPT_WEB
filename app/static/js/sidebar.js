document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggle-sidebar");
    const openButton = document.getElementById("open-sidebar");
    const newChatButton = document.getElementById("new-chat");
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const chatItems = document.querySelectorAll(".chat-item");  // 채팅 아이템 목록
    const chatBox = document.getElementById("chat-box");  // 채팅 메시지 출력 영역
    const messageInputArea = document.querySelector(".message-input-area"); // 입력창 + 버튼 포함 영역

    // ✅ 아이콘 리스트 
    const chatIconList = {
        "애정운": "fa-heart",
        "재물운": "fa-coins",
        "학업운": "fa-pencil",
        "건강운": "fa-dumbbell",
        "미래운": "fa-moon"
    };

    // ✅ 모든 채팅 아이템에 아이콘 추가
    chatItems.forEach(item => {
        const topic = item.getAttribute("data-topic");  // 백엔드에서 보낸 topic 값
        const iconElement = item.querySelector(".chat-icon i");
        
        if (iconElement) {
            const iconClass = chatIconList[topic] || "fa-comments"; // 기본 아이콘 설정
            iconElement.classList.add(iconClass);
        }

        // 🖱️ 채팅 아이템 클릭 이벤트
        item.addEventListener("click", async function() {
            const chatId = item.getAttribute("data-chat-id");  // 클릭된 chat_id 가져오기
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

            // 📌 기존 대화일 경우 입력창과 버튼 숨기기
            messageInputArea.style.display = "none";

        } catch (error) {
            console.error("채팅 메시지 가져오기 실패:", error);
        }
    }

    function confirmDelete(chatId) {
        if (confirm("채팅을 삭제하시겠습니까?")) {
            console.log("채팅 삭제 -> 확인받음")
            fetch(`/chat/delete_chat/${chatId}`, { method: "DELETE" })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("삭제되었습니다.");
                        location.reload(); // 삭제 후 새로고침
                        console.log("삭제 성공");
                    } else {
                        alert("삭제 실패!");
                        console.log("data:", data);
                    }
                })
                .catch(error => console.error("Error:", error));
        }
    }

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

    // 🖱️ 삭제 버튼 클릭 시 채팅 삭제
    deleteButtons.forEach(deleteButton => {
        deleteButton.addEventListener("click", function(event) {
            event.stopPropagation();  // chat-item 클릭 이벤트 방지
            const chatItem = this.closest(".chat-item");
            const chatId = chatItem.getAttribute("data-chat-id");
            confirmDelete(chatId);
        });
    })

    // 🖱️ 새 채팅 버튼 클릭 시 새로고침
    newChatButton.addEventListener("click", function() {
        location.reload();
    })
});
