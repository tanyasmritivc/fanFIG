from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_unfollowers():
    followers_file = request.files['followers']
    following_file = request.files['following']

    try:
        followers_data = json.load(followers_file)
        following_data = json.load(following_file)

        # followers.json is a list of dicts
        followers = set()
        for item in followers_data:
            try:
                username = item["string_list_data"][0]["value"]
                followers.add(username)
            except (KeyError, IndexError):
                continue

        # following.json is a dict with a key 'relationships_following'
        following = set()
        if "relationships_following" in following_data:
            for item in following_data["relationships_following"]:
                try:
                    username = item["string_list_data"][0]["value"]
                    following.add(username)
                except (KeyError, IndexError):
                    continue

        not_following_back = sorted(list(following - followers))

        return jsonify({'not_following_back': not_following_back})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
