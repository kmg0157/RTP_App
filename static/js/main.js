function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const data = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };

                // 서버로 전송
                fetch('/gps', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            },
            function (error) {
                console.error('Error getting location:', error);
            }
        );
    } else {
        alert('Geolocation is not supported by this browser.');
    }
}
