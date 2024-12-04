// Create a map
const container = document.getElementById('map');
const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780), // Seoul, South Korea (center position)
    level: 5
};
const map = new kakao.maps.Map(container, options);

let pathLine = null;  // 경로를 저장할 전역 변수

// 버튼 클릭 이벤트 처리
document.querySelectorAll('.status-button').forEach(button => {
    button.addEventListener('click', function() {
        var isActive = button.classList.contains('active');
        
        // 버튼 상태에 따른 텍스트 변경
        if (isActive) {
            button.textContent = '시작';  // 상태가 초록색이면 "시작"으로 변경
            // '시작' 상태일 때 경로를 삭제
            if (pathLine) {
                pathLine.forEach(line => line.setMap(null));  // 모든 경로 세그먼트를 지도에서 삭제
                pathLine = null;  // 경로 객체 초기화
            }
        } else {
            button.textContent = '측정중'; // 상태가 빨간색이면 "측정중"으로 변경
            // '측정중' 상태일 때 경로를 그리기
            loadCSV('path.csv').then(path => {
                console.log(path);  // 경로 확인
                pathLine = drawPath(path); // 경로 그리기
            }).catch(error => {
                console.error('CSV 로드 실패:', error);  // 에러 처리
            });
        }
    
        // active 클래스 토글
        button.classList.toggle('active');
    
        // 상태 정보 보내기
        sendStatusToBackend(button.textContent === '측정중');
    });
});

function getColorBySaturation(index, total) {
    // 색상 채도를 인덱스에 따라 동적으로 계산
    const saturation = 100 - (index / total) * 100;  // 최신 위치일수록 채도 높음
    return `hsl(0, ${saturation}%, 50%)`;  // 빨간색(HSL)으로 채도만 조정
}

// 경로 그리기 함수
function drawPath(path) {
    const pathLine = [];  // 각 경로 세그먼트를 저장할 배열
    
    // 각 경로의 색상을 계산하고 세그먼트를 추가
    for (let i = 0; i < path.length - 1; i++) {
        const color = getColorBySaturation(i, path.length);  // 색상 계산
        const segment = new kakao.maps.Polyline({
            path: [path[i], path[i + 1]], // 두 점을 연결
            strokeWeight: 10, // 선 두께
            strokeColor: color, // 동적으로 계산된 색상
            strokeOpacity: 1, // 선 투명도
            strokeStyle: 'solid' // 실선
        });
        pathLine.push(segment);  // 경로 세그먼트 배열에 추가
        segment.setMap(map); // 지도에 경로 표시
    }

    // 지도 중심을 경로의 시작점으로 설정
    map.setCenter(path[0]);

    return pathLine; // 여러 개의 경로 세그먼트 배열 반환
}

// CSV 파일을 불러오는 함수
function loadCSV(url) {
    return fetch(url)
        .then(response => response.text())
        .then(csv => {
            const lines = csv.split("\n");
            const path = [];
            for (let i = 1; i < lines.length; i++) {
                const [lat, lng] = lines[i].split(',');
                if (lat && lng) {
                    path.push(new kakao.maps.LatLng(parseFloat(lat), parseFloat(lng)));
                }
            }
            return path;
        });
}

// 상태를 서버로 전송하는 함수 (예시)
function sendStatusToBackend(status) {
    fetch('/api/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: status,  // true(측정중) or false(시작)
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('서버 응답:', data);
    })
    .catch(error => {
        console.error('오류:', error);
    });
}
