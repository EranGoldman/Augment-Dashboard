from flask import Flask, render_template
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
    return dynamodb.download_session(sessionID)


if __name__ == "__main__":
    app.run(debug=True)
