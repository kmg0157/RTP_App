from flask import Flask, render_template, request, jsonify, session, url_for
from flask_cors import CORS
from user_db import register, init_db, id_check
import bcrypt
import os
from werkzeug.utils import redirect


class GPSApp:
    def __init__(self, import_name):
        """
        Flask 앱 초기화 및 설정
        :param import_name: Flask 앱 이름
        """
        self.app = Flask(import_name)
        self.app.secret_key = 'key'
        # init_db() # db
        CORS(self.app)
        self.setup_routes()

    def setup_routes(self):
        """Flask 라우트 정의"""

        @self.app.route('/')
        def index():
            return render_template('register.html')  # 초기화면(회원가입 페이지)
        '''
        @self.app.route('/register',  methods=['POST'])
        def registration():
            data = request.json
            id = data.get('id')
            passwd = data.get('passwd')
            name=data.get('name')
            user_tel=data.get('user_tel')
            target_name=data.get('target_name')
            target_tel=data.get('target_tel')

            # 비밀번호 해싱
            password_hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())

            # 사용자 추가
            if register(id, password_hash, name, user_tel, target_name,target_tel):
                session.clear()
                session['id']=id
                return jsonify({'success': "회원가입 성공",'redirect': url_for('home')}), 200
            else:
                return jsonify({"error": "회원가입 실패"}), 500
          
'''
        @self.app.route('/home', methods=['GET'])
        def home():
           return render_template('home.html')

        @self.app.route('/api/status', methods=['POST'])
        def api_status():
            data=request.get_json()
            print(data)
            return jsonify({'status': "True"}) 


        @self.app.route('/gps', methods=['POST'])
        def receive_gps():
            data = request.get_json()
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            print(f"Received GPS coordinates: Latitude={latitude}, Longitude={longitude}")
            return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})
        

            
        '''
        @self.app.route('/login', methods=['POST'])
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
                #return jsonify({"message": "로그인 성공"}), 200
                return render_template('index.html')
            else:
                return jsonify({"error": "아이디와 패스워드를 확인하시오."}), 401

            '''

    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Flask 서버 실행"""
        self.app.run(host=host, port=port, debug=debug)#, ssl_context=('cert.pem', 'key.pem'))


# 애플리케이션 실행
if __name__ == '__main__':
    gps_app = GPSApp(__name__)
    gps_app.run(debug=True)
