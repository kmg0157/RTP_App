let pathLine = [];  // 경로를 저장할 배열
let currentIndex = 0;  // 현재 그릴 경로의 인덱스
let pathData = [];  // CSV에서 읽은 경로 데이터 저장

// 버튼 클릭 이벤트 처리
document.querySelectorAll('.status-button').forEach(button => {
    button.addEventListener('click', function() {
        var isActive = button.classList.contains('active');
        
        // 버튼 상태에 따른 텍스트 변경
        if (isActive) {
            button.textContent = '시작';  // 상태가 초록색이면 "시작"으로 변경
            // '시작' 상태일 때 경로를 삭제
            button.classList.remove('active');
            pathLine.forEach(line => line.setMap(null));  // 모든 경로 세그먼트를 지도에서 삭제
            pathLine = [];  // 경로 객체 초기화
            currentIndex = 0;  // 인덱스 초기화
        } else {
            button.textContent = '측정중'; // 상태가 빨간색이면 "측정중"으로 변경
            button.classList.add('active');
            
            // '측정중' 상태일 때 경로를 그리기
            loadCSV('static/path.csv').then(path => {
                pathData = path;  // CSV 데이터를 pathData에 저장
                currentIndex = 0;  // 경로 인덱스 초기화
                pathLine = [];  // 경로 배열 초기화
                drawNextPath();  // 첫 번째 경로 그리기
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


// 경로 그리기 함수 (1초마다 경로를 추가하고 채도 업데이트)
function drawNextPath() {
    if (currentIndex < pathData.length) {
        // 경로를 그리기
        const latLng = pathData[currentIndex];
        const nextLatLng = (currentIndex + 1 < pathData.length) ? pathData[currentIndex + 1] : null;

        // 색상 고정
        const color = '#4CAF50';  // 고정된 색상

        const segment = new kakao.maps.Polyline({
            path: [latLng, nextLatLng].filter(Boolean),  // 두 점을 연결, 마지막 점은 없다면 제외
            strokeWeight: 5,  // 선 두께
            strokeColor: color,  // 고정된 색상
            strokeOpacity: 1,  // 선 투명도
            strokeStyle: 'solid'  // 실선
        });

        pathLine.push(segment);  // 경로 세그먼트 배열에 추가
        segment.setMap(map);  // 지도에 경로 표시

        currentIndex++;  // 다음 경로로 이동
        setTimeout(drawNextPath, 800);  // 1초 후 다음 경로 그리기
    }
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
