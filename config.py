from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(
	"mysql+pymysql://root:1111@localhost:3306/myshop",
	pool_size=10, pool_pre_ping=True, echo=True, max_overflow=20)

SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Session = scoped_session(SessionFactory)

def get_session():
	return Session()