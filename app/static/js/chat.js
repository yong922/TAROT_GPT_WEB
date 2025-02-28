document.addEventListener("DOMContentLoaded", function () {
    let messageInput = document.getElementById("message-input");
    let chatBox = document.getElementById("chat-box");
    let sendButton = document.getElementById("send-button");
    let selectedTopic = ""; // ✅ 선택한 토픽 저장 변수
    let firstMessageSent = false;  // 첫 번째 메시지인지 여부


    // ✅ 버튼 클릭 시 메시지 전송
    sendButton.addEventListener("click", sendMessage);

    // ✅ Enter 키 입력 시 메시지 전송
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
    
    // 🟢 메시지를 한 글자씩 출력하는 함수 (stream 방식)
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

            // ✅ 버튼이 필요한 경우, 메시지 내부에 버튼 추가
            if (withButtons) {
                let buttonContainer = createButtonsForChat();
                messageDiv.appendChild(buttonContainer);
            }
    
            resolve(messageDiv); // 메시지 div 반환
        });
    }

    // 🟢 버튼을 생성하는 함수 (단, messageDiv에 추가하도록 변경)
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

        // 1. 서버에 topic 저장
        try {
            const response = await fetch('/chat/topic_update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic: topic })
            });

            if (response.ok) {
                // 2. 서버에 저장된 토픽 확인
                const data = await response.json();
                selectedTopic = data.topic;
                console.log("Topic saved to server:", selectedTopic);

                // 3. 선택된 토픽을 확인하고 메시지 추가
                await addMessageToChatBox(`좋아, ${selectedTopic}에 대해 이야기 해보자. 뭐가 궁금하니?`);
            } else {
                console.error("Filed to save topic to server");
            }
        } catch (error) {
            console.error("Error occurred while saving topic:", error);
        }
    }

    // 🟢 초기 메시지 표시 (stream 방식)
    async function displayBotMessageWithButtons() {
        await addMessageToChatBox("어서오렴. 오늘은 어떤 이야기를 나눠볼까?🧓🏻☕", 50, true);
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
            // const img = document.createElement("img");
            // img.src = cardImagesUrl[card];  // 해당 카드의 이미지 URL
            // img.alt = card;

            // 카드 뒷면 (고정된 뒷면 이미지)
            const backImage = document.createElement("img");
            backImage.src = "/static/imgs/tarot_back_image.jpg";  // 카드 뒷면 이미지
            backImage.alt = "Card Back";
            backImage.classList.add("back");

            // cardElement.appendChild(img);
            // cardContainer.appendChild(cardElement);
            // 카드의 앞면과 뒷면 추가
            cardElement.appendChild(backImage);
            cardElement.appendChild(frontImage);
            cardContainer.appendChild(cardElement);
            
            // // 카드마다 애니메이션을 순차적으로 추가
            // setTimeout(() => {
            //     cardElement.classList.add("flipped");
            // }, index * 200);  // 200ms마다 한 카드씩 보이도록 설정
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

    async function sendMessage() {
        let message = messageInput.value.trim();
        if (!message) return;

        // ✅ 사용자 메시지를 채팅창에 추가
        chatBox.innerHTML += `<div class="message user">${message}</div>`;
        messageInput.value = "";  // 입력창 초기화

        try {
            let cards, cardImagesUrl;

            // ✅ 첫 번째 응답일 경우,
            if (!firstMessageSent) {
                firstMessageSent = true;  // 첫 번째 메시지 처리 후 플래그 설정
                
                // 서버에서 카드 3장과 이미지 URL을 가져옴
                const response = await fetch("/chat/draw_tarot", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" }
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch tarot cards");
                }

                const cardData = await response.json();  // JSON 데이터 파싱
                cards = cardData.cards;  // 뽑힌 카드 배열
                cardImagesUrl = cardData.card_images_url;  // 카드 이미지 URL 객체
                console.log("뽑힌 카드:", cards);
                console.log("카드 URL:", cardImagesUrl);

                displayTarotCards(cards, cardImagesUrl);
            }

            // ✅ 말풍선 생성 (초기 텍스트 없음)
            let botMessage = document.createElement("div");
            botMessage.classList.add("message", "bot");
            chatBox.appendChild(botMessage);            

            // ✅ Flask에 POST 요청
            let response = await fetch("/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
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
        } catch (error) {
            console.error("Error:", error);
        }
    };
});

