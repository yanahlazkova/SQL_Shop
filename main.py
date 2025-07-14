from config import get_session
from models import User, Profile

if __name__ == '__main__':
    Base.metadata.create_all(engine)

session = get_session()
try:
    user = User(name="John", email="2pZ8W@example.com")
    user.profile = Profile(bio="I am a Python developer")
    session.add(user)
    session.commit()
    session.refresh(user)
    print(user.id)
finally:
    session.close()