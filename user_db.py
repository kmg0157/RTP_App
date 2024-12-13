from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 데이터베이스 연결 설정
DATABASE_URL = "mysql+pymysql://root:0313@localhost/rtp_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 사용자 모델 정의
class User(Base):
    __tablename__ = "user_db"

    id = Column(String(20), primary_key=True, nullable=False)
    passwd = Column(String(255), nullable=False)
    name = Column(String(8), nullable=False)
    user_tel=Column(Integer, nullable=False)
    target_name=Column(String(8), nullable=False)
    target_tel=Column(Integer, nullable=False)

#앱 실행 시 테이블 생성하는 초기화 함수
def init_user_db():
    Base.metadata.create_all(bind=engine)

#회원가입 함수
def register(id: str, passwd: str, name: str, user_tel: int, target_name:str, target_tel:int):
    session = SessionLocal()
    try:
        new_user = User(id=id, passwd=passwd, name=name,user_tel=user_tel,target_name=target_name, target_tel=target_tel)
        session.add(new_user)  # 새 사용자 추가
        session.commit()       # 변경 사항 커밋
        return True
    except Exception as e:
        session.rollback()     # 오류 발생 시 롤백
        print(f"Error: {e}")
        return False
    finally:
        session.close()         # 세션 종료

#아이디를 통해 이름 확인
def id_check(id: str):
    session = SessionLocal()
    try:
        return session.query(User).filter(User.id == id).first()
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        session.close()