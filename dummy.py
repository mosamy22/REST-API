from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Survey,User

engine = create_engine('postgresql://survey:survey@localhost/survey')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
survey1 = Survey(name="Mohamed Samy", description="Web Developer",question = ["what is your name","Anything","Anything"],body = 'Anything',note = 'Anything',start_date = '10/10/2019 12:48' ,end_date = '12/10/2019 24:00')
session.add(survey1)
session.commit()

print "added!"
