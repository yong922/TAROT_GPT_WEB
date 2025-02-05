document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.getElementById("menu-icon");

    // WebSocket 연결 설정
    const socket = io.connect('http://localhost:5000');  


    // 사이드바 상태를 저장
    let isSidebarOpen = false;
    // 초기 토픽 값
    let selectedTopic = null;
    
    // 사이드바 열고 닫기 함수
    function toggleSidebar() {
        sidebar.classList.toggle("active");
        isSidebarOpen = !isSidebarOpen;
    }
    // 메뉴 아이콘 클릭 -> 사이드바 열고 닫기
    menuIcon.addEventListener("click", toggleSidebar);


    // 토픽 선택 함수
    function selectTopic(event) {
        // 클릭된 버튼이 토픽 버튼인 경우에만 처리
        if (event.target.classList.contains("topic-btn")) {
            selectedTopic = event.target.textContent;  // 선택된 토픽 설정
            console.log("선택된 토픽:", selectedTopic);

            // 선택된 토픽 버튼에 스타일 추가 (활성화된 토픽 버튼 스타일링)
            const topicButtons = document.querySelectorAll('.topic-btn');
            topicButtons.forEach(btn => btn.classList.remove('active')); // 기존 버튼 스타일 제거
            event.target.classList.add('active'); // 클릭된 버튼에 active 클래스 추가
        }
    }

    // 토픽 버튼 클릭 시 토픽 선택
    const topicButtons = document.querySelectorAll('.topic-btn');
    topicButtons.forEach(btn => {
        btn.addEventListener('click', selectTopic);
    });

    
    // 서버에서 WebSocket을 통해 메시지를 받으면 화면에 표시
    socket.on('new_message', function(data) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${data.sender}`;
        messageDiv.textContent = `${data.message}`;
        chatBox.appendChild(messageDiv);

        // 스크롤을 아래로 이동 (최신 메시지 보이도록)
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    // 메시지 전송 함수 (WebSocket 사용)
    function sendMessage() {
        const userMessage = messageInput.value.trim();

        if (userMessage && selectedTopic) {
            // WebSocket을 통해 서버로 메시지 전송
            socket.emit('send_message', { topic: selectedTopic, text: userMessage });

            // 메시지 입력 필드 초기화
            messageInput.value = '';
        } else {
            alert("토픽을 먼저 선택해주세요!");
        }
    }

    // '전송' 버튼 클릭 시 메시지 전송
    sendButton.addEventListener("click", sendMessage);

    // 'Enter' 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();  // 기본 Enter 동작(줄 바꿈) 방지
            sendMessage();
        }
    });
});

