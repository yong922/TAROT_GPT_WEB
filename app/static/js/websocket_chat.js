document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.getElementById("menu-icon");
    const topicButtons = document.querySelectorAll('.topic-btn');


    // WebSocket 자동 연결 방지
    const socket = io("http://localhost:5000", { autoConnect: false });

    let isSidebarOpen = false;
    let selectedTopic = null;
    let isSocketConnected = false;  // WebSocket이 연결되었는지 확인하는 변수

    // 사이드바 열고 닫기
    function toggleSidebar() {
        sidebar.classList.toggle("active");
        isSidebarOpen = !isSidebarOpen;
    }
    menuIcon.addEventListener("click", toggleSidebar);

    // ✅ 특정 이벤트에서 WebSocket 연결 (예: 토픽 선택 시)
    function connectSocketIfNeeded() {
        if (!isSocketConnected) {
            socket.connect();  // WebSocket 연결
            console.log("WebSocket 연결됨!");
            isSocketConnected = true;  // 연결 상태 업데이트
        }
    }

    // 토픽 선택 함수
    function selectTopic(event) {
        if (event.target.classList.contains("topic-btn")) {
            selectedTopic = event.target.textContent;
            console.log("선택된 토픽:", selectedTopic);

            // 기존 버튼 스타일 제거 후, 선택한 버튼 활성화
            document.querySelectorAll('.topic-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // ✅ 토픽 선택 시 WebSocket 연결 실행
            connectSocketIfNeeded();
        }
    }

    // 토픽 버튼 클릭 시 이벤트 리스너 추가
    document.querySelectorAll('.topic-btn').forEach(btn => btn.addEventListener('click', selectTopic));

    // 서버에서 WebSocket 메시지를 받으면 화면에 추가
    socket.on('new_message', function(data) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${data.sender}`;
        messageDiv.textContent = `${data.message}`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    // 메시지 전송 함수 (WebSocket 사용)
    function sendMessage() {
        if (!selectedTopic) {
            alert("토픽을 먼저 선택해주세요!");
            return;
        }

        const userMessage = messageInput.value.trim();
        if (userMessage) {
            socket.emit('send_message', { topic: selectedTopic, text: userMessage });
            messageInput.value = '';
        }
    }

    // topic 버튼 클릭 이벤트 리스너
    topicButtons.forEach(btn => btn.addEventListener('click', selectTopic));

    // '전송' 버튼 클릭 이벤트 리스너
    sendButton.addEventListener("click", sendMessage);
    // 'Enter' 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});
