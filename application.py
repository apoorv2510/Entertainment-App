from flask import Flask, render_template, request, redirect, url_for, flash, session
from entertainment_lib import get_db_connection, hash_password, verify_password, flash_message
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables
load_dotenv()

# Flask app initialization
app = Flask(__name__)
application = app  # Required for WSGI
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")  # Optional
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
SNS_TOPIC_ARN = os.getenv("AWS_SNS_TOPIC_ARN")
LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "MetricsProcessor")
SQS_QUEUE_URL = os.getenv("AWS_SQS_QUEUE_URL")

# Initialize AWS Clients
sns_client = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

sqs_client = boto3.client(
    "sqs",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
)

# Logging configuration
logging.basicConfig(level=logging.INFO)

# AWS Helper Functions
def send_metric_to_lambda(metric_name, metric_value):
    """Send metrics to the MetricsProcessor Lambda function."""
    payload = {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'namespace': 'RealTimeMetrics'
    }
    try:
        lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType='Event',
            Payload=json.dumps(payload),
        )
        logging.info(f"Metric {metric_name} sent to Lambda successfully.")
    except Exception as e:
        logging.error(f"Failed to send metric: {e}")

def send_login_notification(username):
    """Send a login notification to AWS SNS."""
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"User '{username}' has logged in.",
            Subject="User Login Notification",
        )
        logging.info(f"Login notification sent for user: {username}")
    except ClientError as e:
        logging.error(f"Error sending login notification: {e}")

def send_message_to_sqs(message_body):
    """Send a message to AWS SQS."""
    try:
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message_body),
        )
        logging.info(f"Message sent to SQS: {message_body}")
    except Exception as e:
        logging.error(f"Error sending message to SQS: {e}")
        raise

def send_notification_to_sns(message):
    """Send a notification to AWS SNS."""
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="New Movie Notification",
        )
        logging.info(f"Notification sent to SNS: {message}")
    except Exception as e:
        logging.error(f"Error sending notification to SNS: {e}")

# Flask Routes
@app.context_processor
def inject_user():
    """Inject user data into templates."""
    return {'current_user': session.get('username')}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash_message("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception:
            flash_message("Username already exists!", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and verify_password(user[1], password):
                session['user_id'] = user[0]
                session['username'] = username
                flash_message("Login successful!", "success")
                send_login_notification(username)
                return redirect(url_for('dashboard'))
            else:
                flash_message("Invalid credentials.", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash_message("Logged out successfully.", "success")
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash_message("Please log in to access the dashboard.", "danger")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title, genre, release_year FROM movies")
        movies = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('dashboard.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if 'user_id' not in session:
        flash_message("Please log in to add movies.", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        release_year = request.form['release_year']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO movies (title, genre, release_year) VALUES (%s, %s, %s)",
                (title, genre, release_year)
            )
            conn.commit()

            # Send metrics and notifications
            send_metric_to_lambda('MoviesAdded', 1)
            send_message_to_sqs({"title": title, "genre": genre, "release_year": release_year})
            send_notification_to_sns(f"New Movie Added: {title} ({release_year}) - Genre: {genre}")

            flash_message("Movie added successfully.", "success")
            return redirect(url_for('dashboard'))
        finally:
            cursor.close()
            conn.close()
    return render_template('add_movie.html')

@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if 'user_id' not in session:
        flash_message("Please log in to edit movies.", "danger")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if request.method == 'POST':
            title = request.form['title']
            genre = request.form['genre']
            release_year = request.form['release_year']
            cursor.execute(
                "UPDATE movies SET title = %s, genre = %s, release_year = %s WHERE id = %s",
                (title, genre, release_year, movie_id)
            )
            conn.commit()
            flash_message("Movie updated successfully.", "success")
            return redirect(url_for('dashboard'))
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()
        if not movie:
            flash_message("Movie not found.", "danger")
            return redirect(url_for('dashboard'))
    finally:
        cursor.close()
        conn.close()
    return render_template('edit_movie.html', movie=movie)

@app.route('/delete_movie/<int:movie_id>', methods=['POST', 'GET'])
def delete_movie(movie_id):
    if 'user_id' not in session:
        flash_message("Please log in to delete movies.", "danger")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
        conn.commit()
        flash_message("Movie deleted successfully.", "success")
    except Exception as e:
        flash_message(f"Failed to delete movie: {e}", "danger")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user_id' not in session:
        flash_message("Please log in to upload files.", "danger")
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                file_name = f"user_uploads/{session['user_id']}/{file.filename}"
                s3_client.upload_fileobj(
                    file,
                    AWS_BUCKET_NAME,
                    file_name,
                    ExtraArgs={"ACL": "public-read"}
                )
                file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
                flash_message(f"File uploaded successfully! View it here: <a href='{file_url}' target='_blank'>{file_url}</a>", "success")
            except ClientError as e:
                logging.error(f"Error during file upload: {e}")
                flash_message("An error occurred while uploading the file.", "danger")
        else:
            flash_message("No file selected.", "danger")
    return render_template('upload.html')

@app.route('/view_images')
def view_images():
    if 'user_id' not in session:
        flash_message("Please log in to view uploaded images.", "danger")
        return redirect(url_for('login'))
    try:
        user_prefix = f"user_uploads/{session['user_id']}/"
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=user_prefix)
        images = [
            f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{obj['Key']}"
            for obj in response.get('Contents', [])
        ]
    except ClientError as e:
        logging.error(f"Error listing images: {e}")
        flash_message("Could not retrieve uploaded images.", "danger")
        images = []
    return render_template('view_images.html', images=images)

@app.route('/view_metrics')
def view_metrics_page():
    """Render the metrics display page."""
    return render_template('view_metrics.html')

@app.route('/api/get_metrics', methods=['GET'])
def get_metrics():
    cloudwatch_client = boto3.client("cloudwatch", region_name=AWS_REGION)
    try:
        metrics = cloudwatch_client.list_metrics(Namespace="RealTimeMetrics")
        return {"status": "success", "data": metrics["Metrics"]}, 200
    except Exception as e:
        logging.error(f"Failed to fetch metrics: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
