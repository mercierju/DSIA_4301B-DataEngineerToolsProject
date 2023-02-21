from flask import Flask
from get import get_air_quality_datas
import json
from bson import json_util
from update_datas_bdd import update_datas_db

# Flask permettra de faire communiquer le back et le front via des requètes get dans le front qui vont trigger les
# fonctions à executerdp
app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/')
def test():
    return "Hello wrold!"

# Récupération des donnéees pour les transmettre au front
@app.route('/get_air_quality_datas')
def get_datas():
    datas = get_air_quality_datas()
    return json.loads(json_util.dumps(datas))

# Update des données pour les transmettre au front
@app.route('/update_bdd')
def update_datas():
    return update_datas_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  