from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mysql
from datetime import datetime
from .auth import login_required
import MySQLdb.cursors

transfers_bp = Blueprint('transfers', __name__)

@transfers_bp.route('/transfers')
@login_required
def view_transfers():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("""
        SELECT i.id, i.name, c.cell_number
        FROM inmates i
        LEFT JOIN cells c ON i.cell_id = c.id
        WHERE i.status = 'Active'
    """)
    inmates = cur.fetchall()

    cur.execute("SELECT cell_number FROM cells")
    cells = cur.fetchall()

    cur.execute("""
        SELECT t.*, i.name AS inmate_name 
        FROM transfers t
        JOIN inmates i ON t.inmate_id = i.id
        ORDER BY t.transfer_date DESC
    """)
    transfers = cur.fetchall()

    cur.close()
    return render_template('transfers.html', inmates=inmates, cells=cells, transfers=transfers)

@transfers_bp.route('/transfers/add', methods=['POST'])
@login_required
def add_transfer():
    inmate_id = request.form.get('inmate_id')
    to_cell = request.form.get('to_cell')
    transfer_date = request.form.get('transfer_date')

    if not inmate_id or not to_cell or not transfer_date:
        flash("All fields are required.", "danger")
        return redirect(url_for('transfers.view_transfers'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT c.cell_number, c.id FROM inmates i JOIN cells c ON i.cell_id = c.id WHERE i.id = %s", (inmate_id,))
    result = cur.fetchone()

    if not result:
        flash("Inmate not found.", "danger")
        return redirect(url_for('transfers.view_transfers'))

    from_cell = result['cell_number']
    from_cell_id = result['id']

    cur.execute("SELECT id FROM cells WHERE cell_number = %s", (to_cell,))
    new_cell = cur.fetchone()
    if not new_cell:
        flash("Target cell not found.", "danger")
        return redirect(url_for('transfers.view_transfers'))

    to_cell_id = new_cell['id']

    cur.execute("""
        INSERT INTO transfers (inmate_id, from_cell, to_cell, transfer_date)
        VALUES (%s, %s, %s, %s)
    """, (inmate_id, from_cell, to_cell, transfer_date))

    cur.execute("UPDATE inmates SET cell_id = %s WHERE id = %s", (to_cell_id, inmate_id))
    cur.execute("UPDATE cells SET current_occupancy = current_occupancy - 1 WHERE id = %s", (from_cell_id,))
    cur.execute("UPDATE cells SET current_occupancy = current_occupancy + 1 WHERE id = %s", (to_cell_id,))

    mysql.connection.commit()
    cur.close()

    flash("Transfer completed successfully.", "success")
    return redirect(url_for('transfers.view_transfers'))
