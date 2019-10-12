from flask import Flask, request, jsonify,url_for, abort, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Survey,User
import datetime
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

engine = create_engine('postgresql://survey:survey@localhost/survey')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


#ADD @auth.verify_password decorator here
@auth.verify_password
def verify_password(username_or_token, password):
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

#add /token route here to get a token for a user with login credentials
@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})



@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print "missing arguments"
        abort(400)

    if session.query(User).filter_by(username = username).first() is not None:
        print "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify({'message':'user already exists'}), 200#, {'Location': url_for('get_user', id = user.id, _external = True)}

    user = User(username = username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify({ 'username': user.username }), 201#, {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})




# Create the appropriate app.route functions,
@app.route("/survey", methods = ['GET', 'POST'])
@auth.login_required
def survies():
  if request.method == 'GET':
    #Call the method to Get all of the Survies
    return getAll()
  elif request.method == 'POST':
    #Call the method to make a new Survey
    print ("Posting a New Survey")


    name = request.args.get('name', '')
    description = request.args.get('description', '')
    question = request.args.get('question', '')
    body = questions[0]
    note = questions[1]
    s_date = request.args.get('start_date', '')
    start_date = datetime.datetime.strptime(s_date, '%d-%m-%Y %H:%M')
    e_date = request.args.get('end_date', '')
    end_date = datetime.datetime.strptime(e_date, '%d-%m-%Y %H:%M')
    return makeANewSurvey(name, description,question,body,note,start_date,end_date)

@app.route("/survey/<int:id>", methods = ['GET', 'POST'])
#Call the method to view a specific survey
@auth.login_required
def surveyFunctionId(id):
  if request.method == 'GET':
    return getSurvey(id)


def getAll():
  survies = session.query(Survey).all()
  return jsonify(survies=[i.serialize for i in survies])

def getSurvey(id):
  survey = session.query(Survey).filter_by(id = id).one()
  return jsonify(survey=survey.serialize)

def makeANewSurvey(name,description,question,body,note,start_date,end_date):
  survey = Survey(name = name, description = description,question = question,body = body,note = note,start_date = start_date,end_date = end_date)
  session.add(survey)
  session.commit()
  return jsonify(survey = survey.serialize)




if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
