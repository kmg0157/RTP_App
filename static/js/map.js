// Create a map
const container = document.getElementById('map');
const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780), // Seoul, South Korea (center position)
    level: 3
}; const map = new kakao.maps.Map(container, options);