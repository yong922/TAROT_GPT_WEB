// 사용자가 입력한 메시지+토픽 -> 서버로 전송
// 스트리밍 응답을 받아와서 -> 실시간으로 화면에 표시

document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.getElementById("menu-icon");
    const topicButtons = document.querySelectorAll('.topic-btn');

    let isSidebarOpen = false;  // 사이드바 상태를 저장
    let selectedTopic = "";  // 초기 토픽 값
    let conversationStarted = false;  // 대화 시작 여부
    
    // 초기 상태에서 입력창과 전송 버튼 비활성화
    messageInput.disabled = true;  // 입력창
    sendButton.disabled = true;  // 전송 버튼

    // 사이드바 열고 닫기 함수
    function toggleSidebar() {
        sidebar.classList.toggle("active");
        isSidebarOpen = !isSidebarOpen;
    }

    // 토픽 선택 함수
    function selectTopic(event) {
        if (conversationStarted) return;  // 대화가 시작되면 토픽 변경 불가

        if (!event.target.classList.contains("topic-btn")) return;

        selectedTopic = event.target.textContent;
        console.log("선택된 토픽:", selectedTopic);

        // 모든 토픽 버튼에서 'active' 제거 후 현재 버튼에 추가
        topicButtons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active')

        // 메시지 입력창과 전송 버튼 활성화
        messageInput.disabled = false;
        sendButton.disabled = false;
    }
    

    
    // 메시지 전송 함수 : 사용자 메시지를 서버로 전송, 응답 받아서 화면에 표시
    async function sendMessage() {
        const userMessage = messageInput.value.trim();  // 사용자 메시지 가져오기
        if (userMessage === "") return;  // 메시지가 없으면 무시
        conversationStarted = true;  // 대화 시작 플래그 활성화 (이후 토픽 변경 불가)

        // 사용자 메시지를 채팅창에 추가
        addMessageToUser("user", userMessage);
        messageInput.value = "";  // 입력창 초기화

        // 챗봇 말풍선 생성
        const botMessageElement = addMessageToBot("bot", ""); 
        // updateBotMessage("");  // 챗봇 말풍선 미리 생성
        
        
        // 서버로 스트리밍 요청 보내기
        const response = await fetch("/chat_stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: userMessage, topic: selectedTopic })
        });

        // 스트리밍 응답 처리
        const reader = response.body.getReader();
        const decoder = new TextDecoder();  // 스트림 데이터를 텍스트로 디코딩
        let botMessage = "";  // bot 메시지 저장

        // 스트리밍 데이터 읽기
        while (true) {
            const { done, value } = await reader.read();  // done: 스트림 끝에 도달했는지 여부 / value: 읽은 데이터
            if (done) break;  // 스트림 끝에 도달하면 종료
            
            const chunk = decoder.decode(value, { stream: true });
            botMessage += chunk;

            // 기존 botMessageElement의 내용에 chunk 추가
            botMessageElement.innerHTML += chunk;
            botMessageElement.textContent += chunk;
            // updateBotMessage(botMessage);
        }
    }

    // 챗봇 말풍선에 메시지 추가
    function addMessageToBot(sender, text) {
        const chatBox = document.getElementById("chat-box");
    
        // 🟢 메시지 요소 생성
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    
        // 🟡 말풍선 내용 설정
        messageDiv.innerHTML = text; 
    
        // 🟣 채팅창에 추가
        chatBox.appendChild(messageDiv);
    
        // 🟠 자동 스크롤 (새 메시지가 추가될 때마다)
        chatBox.scrollTop = chatBox.scrollHeight;
    
        return messageDiv; // bot 메시지를 업데이트하기 위해 반환
    }

    // 사용자 말풍선에 메시지 추가
    function addMessageToUser(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // 스트리밍 응답 : bot 메시지 업데이트
    function updateBotMessage(text) {
        let botMessageDiv = document.querySelector(".message.bot:last-child");
        // 마지막 bot 메시지가 없으면 생성
        // if (!botMessageDiv) {
        botMessageDiv = document.createElement("div");
        botMessageDiv.classList.add("message", "bot");
        chatBox.appendChild(botMessageDiv);
        // }
        // 기존 bot 메시지 내부에 실시간 추가
        botMessageDiv.textContent = text;
        chatBox.scrollTop = chatBox.scrollHeight;
    }




    // ===== 이벤트 리스너 =====
    menuIcon.addEventListener("click", toggleSidebar);
    topicButtons.forEach(btn => btn.addEventListener("click", selectTopic));
    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();  // 기본 Enter 동작(줄 바꿈) 방지
            sendMessage();
        }
    });

});