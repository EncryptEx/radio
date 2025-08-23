from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User
from flask_jwt_extended import create_access_token, jwt_required
import telnetlib

host = "liquidsoap"
port = 1234
timeout = 100


main_bp = Blueprint('auth', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'msg': 'username, email and password are required'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'msg': 'username or email already exists'}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'registered', 'user': user.to_dict()}), 201

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'bad credentials'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'user': user.to_dict()})


# Available commands:
# | exit
# | help [<command>]
# | jingles.next
# | jingles.reload
# | jingles.skip
# | jingles.uri [<uri>]
# | music.next
# | music.reload
# | music.skip
# | music.uri [<uri>]
# | output.icecast.metadata
# | output.icecast.remaining
# | output.icecast.skip
# | quit
# | request.all
# | request.metadata <rid>
# | request.resolving
# | request.trace <rid>
# | runtime.gc.compact
# | runtime.gc.full_major
# | runtime.memory
# | shutdown
# | uptime
# | var.get
# | var.list
# | var.set <name> = <value>
# | version

@main_bp.route('/skip', methods=['GET'])
def skip():
    # requires login
    # send telnet command songs.txt
    with telnetlib.Telnet(host, port, timeout) as session:
        session.write(b"music.skip\n")
        session.write(b"exit\n")

    return jsonify({'msg': 'song skipped'}), 200

@main_bp.route('/request', methods=['GET'])
def request_song():
    uri = request.args.get('uri')
    if not uri:
        return jsonify({'msg': 'uri parameter is required'}), 400

    with telnetlib.Telnet(host, port, timeout) as session:
        session.write(f"request.push {uri}\n".encode())
        session.write(b"exit\n")

    return jsonify({'msg': 'request sent'}), 200
