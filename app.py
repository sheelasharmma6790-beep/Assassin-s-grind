from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS enable karna zaroori hai taaki GitHub Pages aur Render aapas me baat kar sakein
CORS(app)

# Global In-Memory Database (Server chalte tak data save rahega)
# Real production me yahan database linked hota hai
agent_database = {}

# Default Server Live Seed Data
server_leaderboard = [
    {"name": "Ayush", "points": 1580, "emoji": "⚡"},
    {"name": "Shorya", "points": 1390, "emoji": "🔥"},
    {"name": "Bhanu", "points": 1240, "emoji": "🔮"},
    {"name": "Honey Chu", "points": 1150, "emoji": "👑"},
    {"name": "Pari", "points": 1060, "emoji": "✨"}
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ONLINE", "message": "Assassin Matrix Backend Protocol is Live!"})

# 1. Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register_agent():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Codename is required"}), 400
    
    # Naya agent initialize ho raha hai backend me
    agent_database[name] = {
        "name": name,
        "age": data.get('age', 18),
        "classUnit": data.get('classUnit', 'Alpha'),
        "points": 0,
        "rank": "5th Rank: Beginner 🛡️ (Belegiam)"
    }
    return jsonify({"message": "Agent registered successfully", "agent": agent_database[name]})

# 2. Points Harvest/Update Endpoint
@app.route('/api/update-points', methods=['POST'])
def update_points():
    data = request.json
    name = data.get('name')
    points_to_add = data.get('points', 0)
    
    if name not in agent_database:
        # Agar browser cache se data aaya par server restart ho gaya tha, toh temporarily recreate karo
        agent_database[name] = {
            "name": name, "age": 20, "classUnit": "Alpha", "points": 0, "rank": "5th Rank"
        }
        
    agent_database[name]['points'] += points_to_add
    pts = agent_database[name]['points']
    
    # Dynamic Rank Calculation on Server Side
    rank_str = "5th Rank: Beginner 🛡️ (Belegiam)"
    if pts >= 200:
        rank_str = "Rank 0: KITUSISUNI 💀 (GOD TIER)"
    elif pts >= 150:
        rank_str = "1st Rank achieved 🤯 (MASTER TIER)"
    elif pts >= 100:
        rank_str = "2nd Rank: Honey Chu tier 👑"
    elif pts >= 60:
        rank_str = "3rd Rank: Shorya tier 🔥"
    elif pts >= 30:
        rank_str = "4th Rank: Ayush tier ⚡"
        
    agent_database[name]['rank'] = rank_str
    return jsonify({"message": "Points synchronized", "agent": agent_database[name]})

# 3. Global Live Leaderboard Endpoint
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # Base leaderboard copy karo
    combined = list(server_leaderboard)
    
    # Backend database ke active players ko leaderboard me merge karo
    for agent_name, agent_info in agent_database.items():
        # Duplicate check bypass karne ke liye
        if not any(player['name'] == agent_name for player in combined):
            combined.append({
                "name": agent_info['name'],
                "points": agent_info['points'],
                "emoji": "🎯",
                "is_live_agent": True
            })
            
    # Points ke basis par highest to lowest sort karo
    combined.sort(key=lambda x: x['points'], reverse=True)
    return jsonify(combined)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
