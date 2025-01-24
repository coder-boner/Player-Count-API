from flask import *
from functools import wraps

app = Flask(__name__)

# This defaults the player counts to 0
database = {"player_count": 0}
mc_database = {"mc_player_count": 0}

# API key (in a real-world scenario, this should be stored securely)
API_KEY = "API_KEY"

# API key function
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') == f"Bearer {API_KEY}":
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return decorated_function

# SCP:SL API, to make more api endpoints copy both GET and PUT pages and give them different urls
@app.route('/scp_sl/plr_count/', methods=['GET'])
def get_player_count():
    return jsonify({"player_count": database["player_count"]})

@app.route('/scp_sl/plr_count/', methods=['PUT'])
@require_api_key
def update_player_count():
    new_count = request.json.get('player_count')
    if new_count is None:
        return jsonify({"error": "player_count is required"}), 400
    database["player_count"] = new_count
    return jsonify({"message": "Player count updated successfully", "player_count": new_count})


# Minecraft API, to make more api endpoints copy both GET and PUT pages and give them different urls
@app.route('/mc/plr_count/', methods=['GET'])
def mc_get_player_count():
    return jsonify({"mc_player_count": mc_database["mc_player_count"]})

@app.route('/mc/plr_count/', methods=['PUT'])
@require_api_key
def mc_update_player_count():
    mc_new_count = request.json.get('mc_player_count')
    if mc_new_count is None:
        return jsonify({"error": "player_count is required"}), 400
    mc_database["mc_player_count"] = mc_new_count
    return jsonify({"message": "Player count updated successfully", "mc_player_count": mc_new_count})

# Html home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(port=8080, debug=True)
