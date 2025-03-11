import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection parameters from environment variables
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_NAME = os.environ.get('POSTGRES_DB', 'flaskapp')
DB_USER = os.environ.get('POSTGRES_USER', 'flaskuser')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password123')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def index():
    return jsonify({
        'message': 'Flask Kubernetes Demo',
        'status': 'running'
    })

@app.route('/health')
def health():
    try:
        # Try to connect to the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)