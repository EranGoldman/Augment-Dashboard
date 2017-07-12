from flask import Flask, render_template, request
app = Flask(__name__)
import dynamodb
# import subprocess

mainData = None

# serveCommand = open("serve.py", "w+")
# dynamodb.download()
# subprocess.Popen(serveCommand)



@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/reload')
def reload_data():
    global mainData
    mainData = None
    return render_template("index.html")

@app.route('/conversations')
def get_data():
    global mainData
    if mainData == None:
        mainData = dynamodb.download()
    return mainData

@app.route('/conversations/<id>')
def load_conversation(id):
    return  render_template("session.html", id = id)

@app.route('/conversations/<sessionID>/get')
def get_conversation(sessionID):
    session_ID = sessionID
    print "running get_conversation with session id = "
    print session_ID
    return dynamodb.download_session(session_ID)


@app.route('/conversations/<sessionIDs>/filter/')
def filterSessions(sessionIDs):
    useAugment = request.args.get('useaugment')
    noAugment =  request.args.get('noaugment')
    haveIntent = request.args.get('haveIntent')
    my_dict = {'useAugment': useAugment, 'haveIntent': haveIntent, 'noAugment': noAugment}
    sessionIDs = sessionIDs
    return dynamodb.filter_session(sessionIDs, my_dict)


if __name__ == "__main__":
    app.run(debug=True)
