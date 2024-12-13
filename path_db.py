import pymysql


def path_checker(path_str):
    # MySQL 데이터베이스 연결 설정
    conn=pymysql.connect(host='localhost', user='root', password='0313', db='rtp_db', charset='utf8')
    
    # 커서 생성
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            sql=f"""
            SELECT EXISTS
                (SELECT 1 FROM path_db WHERE path = %s
            )
            """
            # 쿼리 실행
            cursor.execute(sql, (path_str,))
            result = cursor.fetchone()
            
            # 결과 확인
            if result[0]:
                #존재할 때
                return 'n'
            else:
                return 'an'
    finally:
        conn.close()