function openPopup(message) {
    // 기존 팝업과 오버레이를 제거 (이미 있을 경우)
    const existingOverlay = document.getElementById("overlay");
    if (existingOverlay) existingOverlay.remove();

    // 오버레이 생성
    const overlay = document.createElement('div');
    overlay.id = 'overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.background = 'rgba(0, 0, 0, 0.5)';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = '1000';

    // 팝업 컨테이너 생성
    const popup = document.createElement('div');
    popup.id = 'popup';
    popup.style.background = '#ffffff';
    popup.style.border = '3px solid #e74c3c';
    popup.style.borderRadius = '10px';
    popup.style.width = '320px';
    popup.style.padding = '20px';
    popup.style.textAlign = 'center';
    popup.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';

    // 팝업 내용 추가
    popup.innerHTML = `
        <h3 style="font-size: 18px; font-weight: bold; color: #333; margin: 20px 0;">
            ${message}
        </h3>
        <button id="confirmPath" style="background-color: #4CAF50; color: white; border: none; width: 100%; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 10px;">안심경로 입니다</button>
        <button id="callGuardian" style="background-color: #e74c3c; color: white; border: none; width: 100%; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-bottom: 10px;">피보호자 연락처로 전화걸기</button>
        <button id="callEmergency" style="background-color: #e74c3c; color: white; border: none; width: 100%; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer;">119에 전화걸기</button>
    `;

    // 이벤트 핸들러 연결
    popup.querySelector('#confirmPath').addEventListener('click', () => {
        document.body.removeChild(overlay); // 팝업 닫기
        popupOpened = false; // 플래그 초기화
    });

    popup.querySelector('#callGuardian').addEventListener('click', () => {
        window.location.href = "tel:010-1234-5678"; // 보호자 연락처
    });

    popup.querySelector('#callEmergency').addEventListener('click', () => {
        window.location.href = "tel:119"; // 119 전화
    });

    // 팝업과 오버레이를 body에 추가
    overlay.appendChild(popup);
    document.body.appendChild(overlay);
}
