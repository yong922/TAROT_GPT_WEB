document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("check-button").addEventListener("click", function (event) {
        event.preventDefault(); // 폼 제출 방지
        const userId = document.getElementById("user_id").value; // 입력창 값 가져오기
    
        fetch('/check_id/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // JSON 형식으로 데이터 전송
            },
            body: JSON.stringify({user_id: userId}), // 아이디 데이터 전송
        })

            .then(response => {
                console.log("Response status:", response.status); // 응답 상태 코드 출력
                if (!response.ok) {
                    throw new Error("서버 오류: " + response.status);
                }
                return response.json();
            })
            .then(data => {
                const messageDiv = document.getElementById("id-check-message");
                messageDiv.textContent = data.message; // 메시지 내용 설정
                messageDiv.style.color = data.success ? "green" : "red"; // 색상 설정
            })
            .catch(error => {
                console.error("에러 발생:", error); // 에러 처리
                const messageDiv = document.getElementById("id-check-message");
                messageDiv.textContent = "요청 처리 중 에러가 발생했습니다.";
                messageDiv.style.color = "red";
            });
    });
});