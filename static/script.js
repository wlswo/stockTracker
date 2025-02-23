document.addEventListener('DOMContentLoaded', function () {
    // 모든 변동률 셀을 선택
    const changeCells = document.querySelectorAll('.change-cell');

    changeCells.forEach(cell => {
        let text = cell.textContent.trim();
        // % 기호 제거 후 숫자 변환
        let value = parseFloat(text.replace('%', ''));

        if (!isNaN(value)) {
            if (value > 0) {
                cell.classList.add('heatmap-positive');
            } else if (value < 0) {
                cell.classList.add('heatmap-negative');
            }
        }
    });
});

// Day.js 및 relativeTime 플러그인 로드 후 확장
dayjs.extend(window.dayjs_plugin_relativeTime);

function updateRelativeTimes() {
    const timeElements = document.querySelectorAll('.relative-time');
    timeElements.forEach(function (elem) {
        const rawDate = elem.getAttribute('data-published'); // 예: "20250221T160000"
        // "20250221T160000" 형식을 "2025-02-21 16:00:00"로 변환
        const formattedDate = rawDate.slice(0, 4) + '-' +
            rawDate.slice(4, 6) + '-' +
            rawDate.slice(6, 8) + ' ' +
            rawDate.slice(9, 11) + ':' +
            rawDate.slice(11, 13) + ':' +
            rawDate.slice(13, 15);
        // dayjs로 상대 시간 계산 후 표시 (페이지 로드 시 1회만 계산)
        elem.textContent = dayjs(formattedDate, "YYYY-MM-DD HH:mm:ss").fromNow();
    });
}

// 페이지 로드 시 단 한 번 실행
updateRelativeTimes();