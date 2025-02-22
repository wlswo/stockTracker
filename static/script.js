document.addEventListener('DOMContentLoaded', function() {
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
