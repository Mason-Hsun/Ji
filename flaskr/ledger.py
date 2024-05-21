from flask import Blueprint, render_template, request, abort, jsonify
from database import db

ledger = Blueprint("ledger", __name__)


def check_ledger_name(user_id, ledger_name):
    cursor = db.connect.cursor()
    try:
        cursor.execute(
            f"""
                SELECT *
                FROM Ledgers
                WHERE UID = {user_id}
                AND Lname = '{ledger_name}';
            """
        )
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
            return True
        else:
            return False
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@ledger.route("/insert_ledger", methods=[ "GET", "PUT"])
def insert_ledger():
    user_id = request.args.get("user_id")
    ledger_name = request.args.get("ledger_name")
    cursor = db.connection.cursor()
    if check_ledger_name(user_id, ledger_name):
        return False
    try:
        cursor.execute(
            f"""
                INSERT INTO Ledgers (UID, LName)
                VALUES ({user_id}, '{ledger_name}');
            """
        )
        db.connection.commit()
        cursor.close()
        return True
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@ledger.route("/delete_ledger", methods=["DELETE", "GET"])
def delete_ledger():
    user_id = request.args.get("user_id")
    ledger_name = request.args.get("ledger_name")
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                DELETE FROM Ledgers
                WHERE UID = {user_id}
                AND Lname = '{ledger_name}';
            """
        )
        db.connection.commit()
        cursor.close()
        return True
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@ledger.route("/update_ledger", methods=["PUT", "GET"])
def update_ledger():
    user_id = request.args.get("user_id")
    old_ledger_name = request.args.get("old_ledger_name")
    new_ledger_name = request.args.get("new_ledger_name")
    if check_ledger_name(user_id, new_ledger_name):
        return False
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Ledgers
                SET LName = '{new_ledger_name}'
                WHERE UID = {user_id}
                AND Lname = '{old_ledger_name}';
            """
        )
        db.connection.commit()
        cursor.close()
        return True
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")