from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from datetime import datetime
from flask import Blueprint, current_app, request, make_response
from validators import validate_json, validate_schema
import blueprint.account.schemas as schema
import db
import re

account = Blueprint('account', __name__)


@account.route('/create', methods=['POST'])
@validate_json
@validate_schema(schema.create_schema)
def create():
    payload = request.json
    username = payload['username']
    password = payload['password']

    # Validate inputs
    valid = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
    if not valid.match(username):
        return make_response({
            'success': False,
            'reason': 'Username format is incorrect.'
        }, 400)
    valid = re.compile(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{8,32}$")
    if not valid.match(password):
        return make_response({
            'success': False,
            'reason': 'Password format is incorrect.'
        }, 400)

    # Encode password
    salt = current_app.config.get('PASSWORD_SALT')
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_password = cipher.encrypt(pad(password.encode('utf-8'), cipher.block_size))
    encoded_password = b64encode(ciphered_password).decode('utf-8')
    iv = cipher.iv
    encoded_iv = b64encode(iv).decode('utf-8')

    # Save account data
    conn = current_app.config.get('MYSQL_DB')
    customer_columns = ['username', 'password', 'password_iv', 'password_ver_at', 'updated_at', 'created_at']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cusotmer_values = [f'"{username}"', f'"{encoded_password}"', f'"{encoded_iv}"', f'"{now}"', f'"{now}"', f'"{now}"']
    rows = db.insert(conn=conn, table='customer', columns=customer_columns, values=cusotmer_values, ignore = True)
    if rows == 0:
        return make_response({
            'success': False,
            'reason': 'Username already exists.'
        }, 400)
    return make_response({'success': True}, 200)


@account.route('/verify', methods=['GET'])
@validate_json
@validate_schema(schema.verify_schema)
def verify():
    payload = request.json
    username = payload['username']
    password = payload['password']
    verify_limit = 5

    # Get original password
    conn = current_app.config.get('MYSQL_DB')
    qry = f'''
        SELECT password, password_iv, password_ver_count, password_ver_at
        FROM customer
        WHERE username = "{username}"
    '''
    rows = db.query(conn=conn, qry=qry)
    if len(rows) == 0:
        return make_response({
            'success': False,
            'reason': 'Username or password is incorrect.'
        }, 400)
    password_ver_count = rows[0]['password_ver_count']
    password_ver_at = rows[0]['password_ver_at']
    org_encoded_password = rows[0]['password']
    encoded_iv = rows[0]['password_iv']
    iv = b64decode(encoded_iv.encode('utf-8'))

    # Check verify count
    now = datetime.now()
    timediff = now - password_ver_at
    if password_ver_count >= verify_limit and timediff.total_seconds() < 60:
        return make_response({
            'success': False,
            'reason': 'You have tried 5 times, and try again a minute later.'
        }, 400)

    # Verify password
    salt = current_app.config.get('PASSWORD_SALT')
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphered_password = cipher.encrypt(pad(password.encode('utf-8'), cipher.block_size))
    encoded_password = b64encode(ciphered_password).decode('utf-8')

    if encoded_password != org_encoded_password:
        # Update password verification count
        password_ver_count = password_ver_count + 1 if password_ver_count < verify_limit else 1
        update_columns = ['password_ver_count', 'updated_at']
        update_values = [str(password_ver_count), f'"{now}"']
        if password_ver_count == 5:
            update_columns.append('password_ver_at')
            update_values.append(f'"{now}"')
        where_str = f'username = "{username}"'
        rowcount = db.update(conn=conn, table='customer', columns=update_columns, values=update_values, where_str=where_str)
        if rowcount == 0:
            return make_response({
                'success': False,
                'reason': 'DB fail.'
            }, 400)

        return make_response({
            'success': False,
            'reason': 'Username or password is incorrect.'
        }, 400)

    return make_response({'success': True}, 200)