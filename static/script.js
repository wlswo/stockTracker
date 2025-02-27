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


// 전역 변수에서 값을 가져오거나 기본값을 설정합니다.
let currentPage = window.currentPage || 1;
const sort = window.sort || "importance";
const pageSize = 10;  // 백엔드와 동일하게 설정

function applySort() {
    const selectedSort = document.getElementById("sort-select").value;
    // 정렬 기준 변경 시 페이지 1로 새로고침
    window.location.href = `/news?sort=${selectedSort}&page=1&page_size=${pageSize}`;
}

// 예시: AJAX 응답 후 새 카드 생성
function loadMore() {
    fetch('/api/news?page=' + (window.currentPage + 1) + '&sort=' + window.sort)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-container');
            data.news.forEach(article => {
                const articleElement = document.createElement('article');
                articleElement.className = "bg-white rounded shadow p-4 transition-transform duration-300 transform hover:-translate-y-1 border-2";
                // 중요도 계산 등 추가 처리 (생략)
                articleElement.innerHTML = `
                  <a href="${article.url}" target="_blank">
                    <img src="${article.banner_image}" alt="배너 이미지" class="w-full h-48 object-cover">
                  </a>
                  <h3 class="text-lg font-medium mt-2">
                    <a href="${article.url}" target="_blank" class="hover:underline">${article.title}</a>
                  </h3>
                  <p class="text-sm text-gray-600">${article.summary}</p>
                  <div class="mt-2 flex justify-between text-xs text-gray-500">
                      <span class="published-time" data-time="${article.time_published}"></span>
                      <span>중요도: ${(article.importance_score * 10).toFixed(1)}점</span>
                  </div>
                `;
                container.appendChild(articleElement);
            });
            // 동적으로 추가된 요소에 대해 dayjs 상대 시간 업데이트 실행
            updateRelativeTime();
            window.currentPage++;
        })
        .catch(err => console.error(err));
}
