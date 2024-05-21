from flask import Blueprint, render_template, request, jsonify, abort
from database import db

data = Blueprint("data", __name__, template_folder="flaskr")

@data.route("/get_ledger_datas", methods=["GET"])
def get_ledger_datas():
    user_id = request.args.get("user_id")
    ledger_name = request.args.get("ledger_name")
    cursor = db.connection.cursor()
    cursor.execute(
        f"""
            SELECT *
            FROM Datas
            WHERE UID = {user_id} AND LName = '{ledger_name}'
        """
    )
    result = cursor.fetchall()
    datas = []
    for item in result:
        uid, lname, did, price, dname, dtype, ddate = item
        ddate = ddate.strftime('%Y%m%d')
        datas.append({
            "uid": uid,
            "lname": lname,
            "did": did,
            "price": price,
            "dname": dname,
            "dtype": dtype,
            "ddate": ddate
        })
    cursor.close()
    return jsonify(datas)

@data.route("/insert_new_data", methods=["GET", "POST"])
def insert_new_data():
    try: 
        # Insert new data
        user_id = request.args.get("user_id")
        ledger_name = request.args.get("ledger_name")
        price = request.args.get("price")
        data_name = request.args.get("data_name")
        data_type = request.args.get("data_type")
        data_date = request.args.get("data_date")
        
        cursor = db.connection.cursor()
        
        cursor.execute(
            f"""
                INSERT INTO Datas (UID, LName, Price, DName, DType, DDate)
                VALUES ({user_id}, '{ledger_name}', {price}, '{data_name}', '{data_type}', {data_date});
            """
        )
        cursor.execute("COMMIT")
        
        # Update ledger sum
        cursor.execute(
            f"""
                SELECT LedgerSum
                FROM Ledgers
                WHERE UID = {user_id}
                AND LName = '{ledger_name}'
            """
        )
        result = cursor.fetchone()
        sum = int(result[0]) + int(price)
        cursor.execute(
            f"""
                UPDATE Ledgers
                SET LedgerSum = {sum}
                WHERE UID = {user_id}
                AND LName = '{ledger_name}'
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
        
@data.route("/update_data_name", methods=["GET", "PUT"])
def update_data_name():
    try:
        data_id = request.args.get("data_id")
        data_name = request.args.get("data_name")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                UPDATE Datas
                SET DName = '{data_name}'
                WHERE DID = {data_id}
            """
        )
        cursor.execute("COMMIT")
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")

@data.route("/update_data_price", methods=["GET", "PUT"])
def update_data_price():
    try:
        user_id = request.args.get("user_id")
        ledger_name = request.args.get("ledger_name")
        data_id = request.args.get("data_id")
        price = request.args.get("price")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                UPDATE Datas
                SET Price = {price}
                WHERE DID = {data_id}
            """
        )
        cursor.execute("COMMIT")
        
        # Update ledger sum
        cursor.execute(
            f"""
                SELECT LedgerSum
                FROM Ledgers
                WHERE UID = {user_id}
                AND LName = '{ledger_name}'
            """
        )
        result = cursor.fetchone()
        sum = int(result[0]) + int(price)
        cursor.execute(
            f"""
                UPDATE Ledgers
                SET LedgerSum = {sum}
                WHERE UID = {user_id}
                AND LName = '{ledger_name}'
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
        
@data.route("/update_data_type", methods=["GET", "PUT"])
def update_data_type():
    try:
        data_id = request.args.get("data_id")
        data_type = request.args.get("data_type")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                UPDATE Datas
                SET DType = '{data_type}'
                WHERE DID = {data_id}
            """
        )
        cursor.execute("COMMIT")
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
        
@data.route("/update_data_date", methods=["GET", "PUT"])
def update_data_date():
    try:
        data_id = request.args.get("data_id")
        data_date = request.args.get("data_date")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                UPDATE Datas
                SET DDate = {data_date}
                WHERE DID = {data_id}
            """
        )
        cursor.execute("COMMIT")
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")

@data.route("/delete_data", methods=["GET", "DELETE"])
def delete_data():
    try:
        data_id = request.args.get("data_id")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                DELETE FROM Datas
                WHERE DID = {data_id}
            """
        )
        cursor.execute("COMMIT")
        return True
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
