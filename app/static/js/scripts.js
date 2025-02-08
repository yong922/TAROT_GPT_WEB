document.addEventListener("DOMContentLoaded", function () {
    let idChecked = false; // check 버튼 확인 여부

    const userIdInput = document.getElementById("user_id");
    const messageDiv = document.getElementById("id-check-message");

    userIdInput.addEventListener("input", function () {
        idChecked = false; // 입력이 변경되면 중복 체크 초기화
        messageDiv.innerHTML = ""; // 기존 메시지 삭제
    });

    // check 버튼 클릭 시
    document.getElementById("check-button").addEventListener("click", function (event) {
        event.preventDefault(); // 폼 제출 방지
        const userId = userIdInput.value.trim(); // 입력값 가져오기
        const regex = /^[a-zA-Z0-9]+$/;

        // 1. 입력값이 비어있는 경우
        if (!userId) {
            messageDiv.innerHTML=`
                <div class="alert alert-warning" role="alert">
                    💫 Please enter an ID before checking!
                </div>
            `;
            return;
        }

        // 2. 아이디 길이 조건 (3~20자)
        if (userId.length < 3 || userId.length > 20) {
            messageDiv.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    💫 The ID must be between 3 and 20 characters long.
                </div>
            `;
            return;
        }

        // 3. 영문 숫자만 사용 가능
        if (!regex.test(userId)) {
            messageDiv.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    💫 The ID can only contain letters and numbers.
                </div>
            `;
            return;
        }
    
        // 4. 위 조건 통과시 서버로 중복 체크
        fetch('/check_id/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // JSON 형식으로 데이터 전송
            },
            body: JSON.stringify({user_id: userId}), // 아이디 데이터 전송
        })

        .then(response => {
            if (!response.ok) {
                throw new Error("서버 오류: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            // 기존 메시지 초기화
            messageDiv.innerHTML = "";

            if (data.success) {
                idChecked = true;
                messageDiv.innerHTML = `
                    <div class="alert alert-success" role="alert">
                        💨 ${data.message}
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        🚫 ${data.message}
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error("에러 발생:", error); // 에러 처리
            messageDiv.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    요청 처리 중 에러가 발생했습니다.
                </div>
            `;
        });
    });

    // submit 버튼 클릭 시
    document.getElementById("submit-button").addEventListener("click", function (event) {
        if (!idChecked) {
            event.preventDefault(); // 폼 제출 방지
            const messageDiv = document.getElementById("id-check-message");
            messageDiv.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    💫 Please check the ID first!
                </div>
            `;
        }
    });
});