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

// script.js

// 전역 변수에서 값을 가져오거나 기본값을 설정합니다.
let currentPage = window.currentPage || 1;
const sort = window.sort || "importance";
const pageSize = 10;  // 백엔드와 동일하게 설정

function applySort() {
    const selectedSort = document.getElementById("sort-select").value;
    // 정렬 기준 변경 시 페이지 1로 새로고침
    window.location.href = `/news?sort=${selectedSort}&page=1&page_size=${pageSize}`;
}

async function loadMore() {
    currentPage++;
    try {
        const response = await axios.get('/api/news', {
            params: {
                sort: sort,
                page: currentPage,
                page_size: pageSize
            }
        });
        const newsList = response.data.news;
        const container = document.getElementById("news-container");
        newsList.forEach(article => {
            const articleElem = document.createElement("article");
            articleElem.className = "bg-white rounded shadow p-4";
            articleElem.innerHTML = `
                <img src="${article.banner_image}" alt="배너 이미지" class="w-full h-48 object-cover">
                <h3 class="text-lg font-medium mt-2">${article.title}</h3>
                <p class="text-sm text-gray-600">${article.summary}</p>
            `;
            container.appendChild(articleElem);
        });
        // 만약 추가 데이터가 없으면 "더 보기" 버튼 숨김 처리
        if (newsList.length < pageSize) {
            document.getElementById("load-more-btn").style.display = 'none';
        }
    } catch (error) {
        console.error("데이터 로드 실패:", error);
    }
}
