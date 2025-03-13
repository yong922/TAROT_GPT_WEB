document.addEventListener("DOMContentLoaded", function () {
    let messageInput = document.getElementById("message-input");
    let chatBox = document.getElementById("chat-box");
    let sendButton = document.getElementById("send-button");
    let selectedTopic = ""; 
    let chatId = null;
    let firstMessageSent = false; 


    // ✅ 버튼 클릭 시 메시지 전송
    sendButton.addEventListener("click", sendMessage);

    // ✅ Enter 키 입력 시 메시지 전송
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
    
    // 🟢 메시지를 한 글자씩 출력하는 함수
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

            // 버튼이 필요한 경우, 메시지 내부에 버튼 추가
            if (withButtons) {
                let buttonContainer = createButtonsForChat();
                messageDiv.appendChild(buttonContainer);
            }

            resolve(messageDiv); // 메시지 div 반환
        });
    }

    // 🟢 버튼을 생성하는 함수
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
        selectedTopic = topic;

        // 버튼 비활성화 처리
        document.querySelectorAll(".chat-button").forEach(button => {
            button.disabled = true;
        });

        // 대화창 출력
        await addMessageToChatBox(`좋아, ${selectedTopic}에 대해 이야기 해보자. 뭐가 궁금하니?`);

        // topic 저장
        try {
            const response = await fetch('/chat/set_topic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic })
            });
    
            if (!response.ok) throw new Error("토픽 저장 실패");
            console.log("Topic successfully saved.");
        } catch (error) {
            console.error("Error occurred while saving topic:", error);
        }
    }


    // 🟢 초기 메시지 표시
    async function displayBotMessageWithButtons() {
        await addMessageToChatBox("어서오너라. 오늘은 어떤 이야기를 나눠볼까? 아래에서 선택해보렴.🧓🏻☕", 50, true);
    }

    // 실행
    displayBotMessageWithButtons();


    // 🟢 카드를 화면에 띄우는 함수
    function displayTarotCards(cards, cardImagesUrl) {
        const cardContainer = document.createElement("div");
        cardContainer.classList.add("tarot-cards-container");
        
        cards.forEach((card, index) => {
            const cardElement = document.createElement("div");
            cardElement.classList.add("tarot-card");

            // 카드 앞면 (실제 카드 이미지)
            const frontImage = document.createElement("img");
            frontImage.src = cardImagesUrl[card];  // 카드 앞면 이미지
            frontImage.alt = card;
            frontImage.classList.add("front");
            console.log("카드 이미지 URL:", frontImage.src);

            // 카드 뒷면 (고정된 뒷면 이미지)
            const backImage = document.createElement("img");
            backImage.src = "/static/imgs/tarot_back_image.jpg";  // 카드 뒷면 이미지
            backImage.alt = "Card Back";
            backImage.classList.add("back");

            // 카드의 앞면과 뒷면 추가
            cardElement.appendChild(backImage);
            cardElement.appendChild(frontImage);
            cardContainer.appendChild(cardElement);
            
        });

        document.querySelector("#chat-box").appendChild(cardContainer);

        // 카드 전체를 한꺼번에 등장시키는 애니메이션
        setTimeout(() => {
            // 카드가 한꺼번에 나타남
            document.querySelectorAll(".tarot-card").forEach(card => {
                card.classList.add("visible");
            });

            // 카드가 순차적으로 뒤집히는 애니메이션
            document.querySelectorAll(".tarot-card").forEach((card, index) => {
                setTimeout(() => {
                    card.classList.add("flipped");
                }, 800 + index * 500);  // 첫 번째 카드는 1초 후, 이후 1초 간격으로 뒤집힘
            });

        }, 500);  // 0.5초 후 카드가 한꺼번에 나타남
    }


    // 🟢 chat_id를 가져오는 함수
    async function fetchChatId() {
        try {
            let response = await fetch("/chat/get_latest_chat_id");
            let chatData = await response.json();
            if (chatData.chat_id) {
                chatId = chatData.chat_id;
                console.log("기존 chat_id 가져옴:", chatId);
            }
        } catch (error) {
            console.error("chat_id 가져오기 실패:", error);
        }
    }

    // 🟢 챗봇 응답을 DB에 저장하는 함수
    async function saveBotResponse(chatId) {
        try {
            let response = await fetch("/chat/save_bot_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ chat_id: chatId })
            });

            let result = await response.json();
            console.log("[JS] 챗봇 응답 저장 결과:", result);
        } catch (error) {
            console.error("[JS] 챗봇 응답 저장 실패:", error);
        }
    }
    
    // 🟢 사용자 메시지 전송 함수
    async function sendMessage() {
        let message = messageInput.value.trim();
        if (!message) return;

        // ✅ 사용자 메시지를 채팅창에 추가
        chatBox.innerHTML += `<div class="message user">${message}</div>`;
        messageInput.value = "";  // 입력창 초기화

        let cards, cardImagesUrl;

        // ✅ 첫 번째 응답일 경우
        if (!firstMessageSent) {
            firstMessageSent = true;  
            
            try{
                const response = await fetch("/chat/draw_tarot", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch tarot cards");
                }

                const cardData = await response.json();
                cards = cardData.cards;
                cardImagesUrl = cardData.card_images_url;

                console.log("뽑힌 카드:", cards);
                console.log("카드 URL:", cardImagesUrl);

                displayTarotCards(cards, cardImagesUrl);
            } catch (error) {
                console.error("[ERROR] 타로 카드 가져오기 실패:", error);
                return;  // 에러 발생 시 진행 중단 (응답 없이 종료)
            }
        }

        // ✅ 말풍선 생성 (초기 텍스트 없음)
        let botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");
        chatBox.appendChild(botMessage);

        try {
            // ✅ Flask에 POST 요청
            let response = await fetch("/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, topic: selectedTopic, chat_id: chatId })
            });

            if (!response.ok) {
                throw new Error("Failed to fetch response from chat API");
            }

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

            // chatId 가져오기
            if (!chatId) {
                await fetchChatId();
            }

            await saveBotResponse(chatId);
        } catch (error) {
            console.error("Error:", error);
        }
    }
});

