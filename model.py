from sqlalchemy import Column, Integer, String ,ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import json
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()


# this secret key to create and verify your tokens
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    #Add a method to generate auth tokens here
    def generate_auth_token(self, expiration=600):
    	s = Serializer(secret_key, expires_in = expiration)
    	return s.dumps({'id': self.id })
    #Add a method to verify auth tokens here
    @staticmethod
    def verify_auth_token(token):
    	s = Serializer(secret_key)
    	try:
    		data = s.loads(token)
    	except SignatureExpired:
    		#Valid Token, but expired
    		return None
    	except BadSignature:
    		#Invalid Token
    		return None
    	user_id = data['id']
    	return user_id


class Survey(Base):
    __tablename__ = 'posts'


    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    question = Column(ARRAY(String))
    body = Column(String(250))
    note = Column(String(250))
    start_date = Column(String(250))
    end_date = Column(String(250))
    #Add add a decorator property to serialize data from the database
    @property
    def serialize(self):

       return {
           'name'         : self.name,
           'id'         : self.id,
           'description'         : self.description,
           'question'         : self.question,
           'body'         : self.body,
           'note'         : self.note,
           'start_date'         : self.start_date,
           'end_date'          : self.end_date
       }



engine = create_engine('postgresql://survey:survey@localhost/survey')
Base.metadata.create_all(engine)
