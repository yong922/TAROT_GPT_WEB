document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggle-sidebar");
    const openButton = document.getElementById("open-sidebar");

    // 닫기 버튼 클릭 시 사이드바 닫기
    toggleButton.addEventListener("click", function () {
        sidebar.classList.remove("open");
        sidebar.classList.add("closed");
    });

    // 사이드바 버튼 클릭 시 사이드바 열기
    openButton.addEventListener("click", function () {
        sidebar.classList.remove("closed");
        sidebar.classList.add("open");
    });
});
