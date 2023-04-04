from flask import Blueprint, current_app, request, make_response
from datetime import datetime
from jsonschema import validate
import db

point = Blueprint('point', __name__)

@point.route('/add', methods=['POST'])
def add(customer_id):
    # Validate payload
    payload = request.json
    schema = {
        "type" : "object",
        "properties" : {
            "amount" : {"type" : "number"}
        }
    }
    try:
        validate(instance=payload, schema=schema)
    except:
        return make_response({'message': 'Failed'}, 400)
    
    amount = payload['amount']
    if amount <= 0:
        return make_response({'message': 'Failed'}, 400)
    
    # Add points
    conn = current_app.config.get('MYSQL_DB')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_columns = ['amount', 'updated_at']
    update_values = [f'amount + {amount}', f'"{now}"']
    where_str = f'customer_id = {customer_id}'
    rowcount = db.update(conn=conn, table='point', columns=update_columns, values=update_values, where_str=where_str)
    if rowcount == 0:
        return make_response({'message': 'Failed'}, 400)
    
    # Record Log
    log_columns = ['customer_id', 'amount', 'action', 'created_at']
    log_values = [str(customer_id), str(amount), '"ADD"', f'"{now}"']
    db.insert(conn=conn, table='point_change_history', columns=log_columns, values=log_values)
    return make_response({'message': 'success'}, 200)

@point.route('/redeem', methods=['POST'])
def redeem(customer_id):
    payload = request.json

    # Validate payload
    schema = {
        "type" : "object",
        "properties" : {
            "commodities" : {
                "type": "array",
                "items": {
                    "commodity_id" : {"type" : "number"},
                    "amount" : {"type" : "number"}
                }
            }
        }
    }
    try:
        validate(instance=payload, schema=schema)
    except:
        return make_response({'message': 'Failed'}, 400)

    # Calculate cost
    commodities = payload['commodities']
    com_id_str = ', '.join([str(e['commodity_id']) for e in commodities])
    conn = current_app.config.get('MYSQL_DB')
    qry = f'''
        SELECT id, cost
        FROM commodity
        WHERE id in ({com_id_str})
    '''
    rows = db.query(conn=conn, qry=qry)
    hashmap = {r['id']: r['cost'] for r in rows}
    cost = 0
    for c in commodities:
        cost += hashmap[c['commodity_id']] * c['amount']

    # Redeem
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_columns = ['amount', 'updated_at']
    update_values = [f'amount - {cost}', f'"{now}"']
    where_str = f'customer_id = {customer_id} AND (amount - {cost}) >= 0'
    rowcount = db.update(conn=conn, table='point', columns=update_columns, values=update_values, where_str=where_str)
    if rowcount == 0:
        return make_response({'message': 'Failed'}, 400)

    # Record Log
    log_columns = ['customer_id', 'amount', 'action', 'created_at']
    log_values = [str(customer_id), str(-cost), '"REDEEM"', f'"{now}"']
    db.insert(conn=conn, table='point_change_history', columns=log_columns, values=log_values)
    return make_response({'message': 'success'}, 200)