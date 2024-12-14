let pathLine = [];  // 경로를 저장할 배열
let pathData = [];  // CSV에서 읽은 경로 데이터 저장
let currentIndex = 0;  // 현재 그릴 경로의 인덱스

// 가짜 버튼
document.querySelectorAll('.status-button').forEach(button => {
    button.addEventListener('click', function() {
        var isActive = this.classList.contains('active');
        if (isActive) { button.textContent = '시작'; } 
        else { button.textContent = '측정중'; }
        button.classList.toggle('active');
    });
});

// status 버튼
document.querySelector('#real-status-button').addEventListener('click', function() {
    var isActive = this.classList.toggle('active'); //버튼 토글
    

    if (isActive) {// 측정중
        this.textContent = '측정중';

        // 경로 그리기
        loadCSV('./static/path.csv').then(path => {
            pathData = path;  // CSV 데이터를 pathData에 저장
            pathLine = [];  
            isDrawing = true;
            drawNextPath();  

            // 지도 중심과 레벨 변경 (최초 1번)
            map.setCenter(pathData[currentIndex]);
            map.setLevel(2);

        }).catch(error => {
                console.error('CSV 로드 실패:', error);});
    } 
    else {// 시작
        this.textContent = '시작';
        sendStatusToBackend(false,0,0); // 상태 정보 보내기
        isDrawing = false; // 경로 그리기 중지
        pathLine.forEach(line => line.setMap(null)); //지도 지우기
        pathLine = [];  // 경로 객체 초기화
    }
});



// 경로 그리기 함수 (1초마다 경로를 추가하고 채도 업데이트)
function drawNextPath() {
    if (currentIndex < pathData.length && isDrawing) {
        
        // 위치 변수
        const latLng = pathData[currentIndex];
        const nextLatLng = (currentIndex + 1 < pathData.length) ? pathData[currentIndex + 1] : null;

        //서버에 전송송
        sendStatusToBackend(true,latLng.La,latLng.Ma);

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


//서버 통신
let popupOpened = false; // 팝업이 열렸는지 여부
let ignorePopupCount = 0; // 이후 무시할 응답 횟수 카운터

function sendStatusToBackend(active, lat, lng) {
    fetch('/api/status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            status: active,  // true(측정중) or false(시작)
            lat: lat,
            lng: lng
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('서버 응답:', data);

        // 팝업 무시 카운터가 남아있으면 카운터를 감소시키고 종료
        if (ignorePopupCount > 0) {
            ignorePopupCount--;
            console.log(`팝업 무시: 남은 카운트 ${ignorePopupCount}`);
            return;
        }

        // 상태가 'n'이고 팝업이 아직 안 열렸다면 팝업 열기
        if (data.status === 'n' && !popupOpened) {
            popupOpened = true; 
            openPopup(data.message || "서버 상태가 n 입니다. 계속 진행할까요?");
        }
    })
    .catch(error => {
        console.error('오류:', error);
    });
}


