//  // 버튼 클릭 이벤트 처리
//         // 모든 status-btn 버튼에 대해 이벤트 리스너를 추가
//         document.querySelectorAll('.status-btn').forEach(button => {
//             button.addEventListener('click', function() {
//                 var isActive = button.classList.contains('active');
                
//                 // 버튼 상태에 따른 텍스트 변경
//                 if (isActive) {
//                     button.textContent = '시작';  // 상태가 초록색이면 "시작"으로 변경
//                 } else {
//                     button.textContent = '측정중'; // 상태가 빨간색이면 "측정중"으로 변경
//                 }
    
//                 // 상태 토글: active 클래스를 추가하거나 제거
//                 button.classList.toggle('active');
    
//                 // 백엔드로 상태 정보 보내기 (AJAX 사용 예시)
//                 sendStatusToBackend(button.textContent === '측정중');
//             });
//         });
    
//         // AJAX 요청을 보내는 함수
//         function sendStatusToBackend(status) {
//             fetch('/api/status', {  // 예시 URL, 실제 URL로 변경해야 합니다.
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({
//                     status: status,  // true(측정중) or false(시작)
//                 }),
//             })
//             .then(response => response.json())
//             .then(data => {
//                 console.log('서버 응답:', data);
//             })
//             .catch(error => {
//                 console.error('오류:', error);
//             });
//         }