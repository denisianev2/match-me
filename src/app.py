from dotenv import load_dotenv
from flask import Flask
from modules.utils.utils import validate_env
from modules.user.controller import user_bp
from modules.matching.controller import matching_bp
from modules.common.controller import common_bp
from modules.mentor.controller import mentor_bp
from modules.mentee.controller import mentee_bp
from flask_cors import CORS

load_dotenv()
validate_env()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


app.register_blueprint(user_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(common_bp)
app.register_blueprint(mentor_bp)
app.register_blueprint(mentee_bp)


if __name__ == "__main__":
    app.run(port=3000, host="127.0.0.1", debug=True)
