from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#데이터베이스 관련된 인증 정보를 상수로 선언함.
DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"


#sqlalchemy를 활용해 데이터에 접근하려면 engine 필요
engine = create_engine(DATABASE_URL, echo=True)   #echo=True: sqlalchemy에 의해 쿼리가 처리될 때, 사용된 쿼리를 프린트해주는 옵션. 디버깅 시 활용됨.
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


