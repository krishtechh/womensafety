from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus

app = Flask(__name__)

# Database configuration with password encoding
db_username = "root"  # Replace with your MySQL username
db_password = "Eshabatra@29"  # Your actual password
db_name = "userdata"  # Your database name

# URL-encode the password to handle special characters
encoded_password = quote_plus(db_password)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{encoded_password}@localhost:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this for production!

db = SQLAlchemy(app)

# User model matching your table structure
class User(db.Model):
    __tablename__ = 'information'
    
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # Your existing HTML file

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('txt')
        email = request.form.get('email')
        password = request.form.get('pswd')
        phone = request.form.get('phone')
        
        # Hash the password before storing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                phone_number=phone
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('success'))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}", 400

# Change your success route to render the template directly
@app.route('/success')
def success():
    return render_template('favcontact.html')  # Directly render instead of redirect

# Add this route to handle direct requests to favcontact.html
@app.route('/favcontact.html')
def favcontact():
    return render_template('favcontact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
    app.run(debug=True)