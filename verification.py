from database import db_session,select, Website,User


def verify_user(username,password):
    q = select(User).filter_by(username=username)
    with db_session() as sess:
        user=sess.scalar(q)
    if user and user.password == password:
        return user
    return False
            



def domain_exists(domain):
    q = select(Website).filter_by(domain=domain)
    with db_session() as sess:
        if sess.scalar(q):
            return True
    return False
