from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from user_db import register, init_db, id_check
import bcrypt

class GPSApp:
    def __init__(self, import_name):
        """
        Flask 앱 초기화 및 설정
        :param import_name: Flask 앱 이름
        """
        self.app = Flask(import_name)
        self.app.secret_key = 'key'
        init_db()
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
        
        @self.app.route('/register/',  methods=['POST'])
        def registration():
            data = request.json
            id = data.get('id')
            passwd = data.get('passwd')
            name=data.get('name')
            user_tel=data.get('user_tel')
            target=data.get('target')
            target_tel=data.get('target_tel')

            # 입력 검증
            if not id or not passwd:
                return jsonify({"error": "아이디 패스워드를 확인하시오."}), 400

            # 비밀번호 해싱
            password_hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

            # 사용자 추가
            if register(id, password_hash, name, user_tel, target,target_tel):
                return jsonify({"message": "회원가입 성공"
                                , "id":{id}
                                , "password_hash":{password_hash}
                                , "name":{name}
                                , "user_tel":{user_tel}
                                , "target":{target}
                                , "target_tel":{target_tel}
                                }), 201
            else:
                return jsonify({"error": "회원가입 실패"}), 500  
            
                
        @self.app.route('/login/', methods=['POST'])
        def login():
            data = request.json
            id = data.get('id')
            passwd = data.get('passwd')
            
            # 입력 데이터 검증
            if not id or not passwd:
                return jsonify({"error": "아이디와 패스워드를 확인하시오."}), 400
            
            # 사용자 인증 로직
            User=id_check(id)
            if User and bcrypt.checkpw(passwd.encode('utf-8'), User.password_hash.encode('utf-8')):
                return jsonify({"message": "로그인 성공"}), 200
            else:
                return jsonify({"error": "아이디와 패스워드를 확인하시오."}), 401

            

    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Flask 서버 실행"""
        self.app.run(host=host, port=port, debug=debug, ssl_context=('cert.pem', 'key.pem'))


# 애플리케이션 실행
if __name__ == '__main__':
    gps_app = GPSApp(__name__)
    gps_app.run()
