document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const sidebar = document.getElementById("sidebar");
    const menuIcon = document.getElementById("menu-icon");
    const topicButtons = document.querySelectorAll('.topic-btn');


    // WebSocket 연결 설정
    const socket = io.connect('http://localhost:5000');  

    let isSidebarOpen = false;  // 사이드바 상태를 저장
    let selectedTopic = null;  // 초기 토픽 값
    let conversationStarted = false;  // 대화 시작 여부
    
    // 초기 상태에서 입력창과 전송 버튼 비활성화
    messageInput.disabled = true;  // 입력창
    sendButton.disabled = true;  // 전송 버튼


    // ===========사이드바===========
    // 사이드바 열고 닫기 함수
    function toggleSidebar() {
        sidebar.classList.toggle("active");
        isSidebarOpen = !isSidebarOpen;
    }
    // 메뉴 아이콘 클릭 -> 사이드바 열고 닫기
    menuIcon.addEventListener("click", toggleSidebar);


    // ===========토픽===========
    // 토픽 버튼 클릭 시 토픽 선택
    // topicButtons.forEach(btn => {
    //     btn.addEventListener('click', selectTopic);
    // });
    // 토픽 선택 함수
    function selectTopic(event) {
        // 대화가 시작되면 토픽 변경 불가
        if (conversationStarted) return;

        if (!event.target.classList.contains("topic-btn")) return;

        // 이미 선택된 토픽이면 무시 (메시지 전송 후 버튼이 비활성화됨)
        // if (event.target.classList.contains('disabled')) return;

        selectedTopic = event.target.textContent;
        console.log("선택된 토픽:", selectedTopic);

        // 모든 토픽 버튼에서 'active' 제거 후 현재 버튼에 추가
        topicButtons.forEach(btn => btn.classList.remove('active'));  // 버튼 상태 초기화
        event.target.classList.add('active')  // 선택한 버튼 활성화

        // 메시지 입력창과 전송 버튼 활성화
        messageInput.disabled = false;
        sendButton.disabled = false;

        // if (event.target.classList.contains("topic-btn")) {
        //     selectedTopic = event.target.textContent;  // 선택된 토픽 설정
        //     console.log("선택된 토픽:", selectedTopic);

        //     // 선택된 토픽 버튼에 스타일 추가 (활성화된 토픽 버튼 스타일링)
        //     const topicButtons = document.querySelectorAll('.topic-btn');
        //     topicButtons.forEach(btn => btn.classList.remove('active')); // 기존 버튼 스타일 제거
        //     event.target.classList.add('active'); // 클릭된 버튼에 active 클래스 추가
        // }
    }


    // 메시지를 화면에 추가하는 함수
    function addMessage(role, content) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${role}`;
        messageDiv.textContent = content;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;  // 자동 스크롤
        return messageDiv;  // 생성된 메시지 요소 반환
    }
    
    // 서버에서 WebSocket을 통해 메시지를 받으면 화면에 표시
    // "new_message" 이벤트 : user/bot의 메시지를 한번에 표시
    socket.on('new_message', function(data) {
        // const messageDiv = document.createElement("div");  // 새 div 요소 생성
        // messageDiv.className = `message ${data.sender}`;  // 'message user' 또는 'message bot' 클래스를 부여
        // messageDiv.textContent = `${data.message}`;  // 메시지 내용을 설정
        // chatBox.appendChild(messageDiv);  // 채팅 박스에 추가
        if (data.sender === "user") {
            // user 메시지, 서버에서 받은 메시지를 화면에 추가
            addMessage("user", data.message);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // 스크롤을 아래로 이동 (최신 메시지 보이도록)
        // chatBox.scrollTop = chatBox.scrollHeight;
    });

    // 서버에서 WebSocket을 통해 메시지를 스트리밍 방식으로 받음
    socket.on('stream_message', function(data) {
        let botMessageDiv = document.querySelector(".message.bot:last-child"); 
        console.log("stream_message 이벤트 리스너 실행");
        if (!botMessageDiv) {  // 새 메시지가 없을 때 -> 새로운 div를 생성하도록
            botMessageDiv = addMessage("bot", "");  // 새로운 메시지 요소 추가
        }

        botMessageDiv.textContent += data.chunk;  // 받은 chunk 추가
    });

    // 메시지 전송 함수 (WebSocket 사용)
    function sendMessage() {
        const userMessage = messageInput.value.trim();

        if (userMessage && selectedTopic) {
            // 사용자 메시지 화면에 추가
            addMessage("user", userMessage);

            // WebSocket을 통해 서버(routes.py)로 메시지 전송
            socket.emit('send_message', { topic: selectedTopic, text: userMessage });

            // 메시지 입력 필드 초기화
            messageInput.value = '';

            // 첫 메시지 전송 -> 대화 시작, 토픽 변경 금지
            if (!conversationStarted) {
                conversationStarted = true;
                            // 메시지 전송 후 -> 선택안된 버튼 비활성화화
                topicButtons.forEach(btn => {
                    if (!btn.classList.contains('active')) {
                        btn.classList.add('disabled');  // 선택되지 않은 버튼 클릭 불가능
                    }
                });
            }
        } else {
            alert("토픽을 먼저 선택해주세요!");
        }
    }

    // topic 버튼 클릭 이벤트 리스너
    topicButtons.forEach(btn => btn.addEventListener('click', selectTopic));

    // '전송' 버튼 클릭 이벤트 리스너
    sendButton.addEventListener("click", sendMessage);
    // 'Enter' 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();  // 기본 Enter 동작(줄 바꿈) 방지
            sendMessage();
        }
    });
});

