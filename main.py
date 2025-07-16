import os
# from dotenv import load_dotenv

# Загружаем переменные из .env файла
# load_dotenv()
# 
# POOL = pooling.MySQLConnectionPool(
#     host=os.environ.get('DB_HOST'),
#     port=os.environ.get('DB_PORT'),
#     user=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PASSWORD'),
#     pool_name='pool1',
#     pool_size=5)


from config import engine, get_session
from models import Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)

session = get_session()


# try:
#     user = User(name="John", email="2pZ8W@example.com")
#     user.profile = Profile(bio="I am a Python developer")
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     print(user.id)
# finally:
#     session.close()

