import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'instance/sentiment_app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_id TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracker_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_id TEXT NOT NULL,
            views_plot_path TEXT,
            likes_plot_path TEXT,
            subscribers_plot_path TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def create_user(username, email, password):
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def verify_user(email, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def add_prediction(user_id, video_id, sentiment):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO predictions (user_id, video_id, sentiment) VALUES (?, ?, ?)',
        (user_id, video_id, sentiment)
    )
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def get_user_predictions(user_id, limit=None):
    conn = get_db()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute(
            'SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
            (user_id, limit)
        )
    else:
        cursor.execute(
            'SELECT * FROM predictions WHERE user_id = ? ORDER BY timestamp DESC',
            (user_id,)
        )
    
    predictions = cursor.fetchall()
    conn.close()
    return [dict(pred) for pred in predictions]

def get_sentiment_stats(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT sentiment, COUNT(*) as count FROM predictions WHERE user_id = ? GROUP BY sentiment',
        (user_id,)
    )
    stats = cursor.fetchall()
    conn.close()
    return {stat['sentiment']: stat['count'] for stat in stats}

def add_tracker_history(user_id, video_id, plots):
    conn = get_db()
    cursor = conn.cursor()
    
    plot_paths = {
        'views': None,
        'likes': None,
        'subscribers': None
    }
    for plot in plots:
        if 'views' in plot:
            plot_paths['views'] = plot
        elif 'likes' in plot:
            plot_paths['likes'] = plot
        elif 'subscribers' in plot:
            plot_paths['subscribers'] = plot

    cursor.execute(
        'INSERT INTO tracker_history (user_id, video_id, views_plot_path, likes_plot_path, subscribers_plot_path) VALUES (?, ?, ?, ?, ?)',
        (user_id, video_id, plot_paths['views'], plot_paths['likes'], plot_paths['subscribers'])
    )
    conn.commit()
    history_id = cursor.lastrowid
    conn.close()
    return history_id

def get_tracker_history(user_id, limit=3):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM tracker_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?',
        (user_id, limit)
    )
    history = cursor.fetchall()
    conn.close()
    return [dict(row) for row in history]


if __name__ == '__main__':
    import os
    os.makedirs('instance', exist_ok=True)
    init_db()
