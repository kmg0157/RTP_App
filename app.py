from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

class GPSApp:
    def __init__(self, import_name):
        """
        Flask 앱 초기화 및 설정
        :param import_name: Flask 앱 이름
        """
        self.app = Flask(import_name)
        CORS(self.app)
        self.setup_routes()

    def setup_routes(self):
        """Flask 라우트 정의"""
        @self.app.route('/')
        def home():
            return render_template('index.html')  # 클라이언트에 HTML 파일 제공

        @self.app.route('/gps', methods=['POST'])
        def receive_gps():
            data = request.get_json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            print(f"Received GPS coordinates: Latitude={latitude}, Longitude={longitude}")
            return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})

            

    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Flask 서버 실행"""
        self.app.run(host=host, port=port, debug=debug, ssl_context=('cert.pem', 'key.pem'))


# 애플리케이션 실행
if __name__ == '__main__':
    gps_app = GPSApp(__name__)
    gps_app.run()
