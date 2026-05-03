from app import db

# Example models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'jailer'), nullable=False)
    last_notification_check = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Inmate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crime = db.Column(db.String(255), nullable=False)
    sentence_duration = db.Column(db.String(50), nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    release_date = db.Column(db.Date)
    status = db.Column(db.Enum('Active', 'Released'), default='Active')
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.Enum('Release', 'Medical', 'Security'), nullable=False)
    message = db.Column(db.Text)
    alert_date = db.Column(db.Date)
    status = db.Column(db.Enum('Active', 'Resolved'), default='Active')
    inmate_id = db.Column(db.Integer, db.ForeignKey('inmate.id'))