from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
import time

# Available avatars - 3 free, 7 locked
AVATARS = [
    {'id': 1, 'name': 'Forest Fox', 'locked': False, 'points_required': 0},
    {'id': 2, 'name': 'Lake Turtle', 'locked': False, 'points_required': 0},
    {'id': 3, 'name': 'Mountain Bear', 'locked': False, 'points_required': 0},
    {'id': 4, 'name': 'River Otter', 'locked': True, 'points_required': 50},
    {'id': 5, 'name': 'Forest Owl', 'locked': True, 'points_required': 100},
    {'id': 6, 'name': 'Meadow Rabbit', 'locked': True, 'points_required': 150},
    {'id': 7, 'name': 'Ocean Whale', 'locked': True, 'points_required': 200},
    {'id': 8, 'name': 'Sky Eagle', 'locked': True, 'points_required': 250},
    {'id': 9, 'name': 'Garden Butterfly', 'locked': True, 'points_required': 300},
    {'id': 10, 'name': 'Crystal Dragon', 'locked': True, 'points_required': 350}
]

WELLNESS_TASKS = [
    {'id': 1, 'name': 'Read a Book', 'description': 'Take time to read and expand your mind'},
    {'id': 2, 'name': 'Meditate', 'description': 'Practice mindfulness and inner peace'},
    {'id': 3, 'name': 'Take a Walk', 'description': 'Get some fresh air and exercise'},
    {'id': 4, 'name': 'Drink Water', 'description': 'Stay hydrated for better health'},
    {'id': 5, 'name': 'Deep Breathing', 'description': 'Practice breathing exercises to reduce stress'}
]

@app.route('/')
def login():
    return render_template('login.html', avatars=AVATARS)

@app.route('/register', methods=['POST'])
def register():
    # Get form data
    name = request.form.get('name')
    age = request.form.get('age')
    screen_time = request.form.get('screen_time')
    avatar_id = request.form.get('avatar_id')
    
    # Validate data
    if not all([name, age, screen_time, avatar_id]):
        return redirect(url_for('login'))
    
    # Store user data in session
    session['user'] = {
        'name': name,
        'age': int(age or 18),
        'screen_time': float(screen_time or 0),
        'avatar_id': int(avatar_id or 1),
        'points': 0,
        'unlocked_avatars': [1, 2, 3],  # First 3 avatars are free
        'most_used_app': '',
        'task_completions': {},
        'study_sessions': 0,
        'total_wellness_time': 0  # Track total time spent on wellness tasks
    }
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    
    # Ensure total_wellness_time exists for backward compatibility
    if 'total_wellness_time' not in user:
        user['total_wellness_time'] = 0
    
    # Update unlocked avatars based on points (every 50 points unlocks a new avatar)
    points = user.get('points', 0)
    unlocked = [1, 2, 3]  # Always unlocked
    # Calculate how many avatars should be unlocked (every 50 points)
    avatars_to_unlock = min(points // 50, 7)  # Maximum 7 additional avatars
    for i in range(avatars_to_unlock):
        if i + 4 <= 10:  # Avatar IDs 4-10
            unlocked.append(i + 4)
    
    user['unlocked_avatars'] = unlocked
    session['user'] = user
    
    # Get current avatar
    current_avatar = next((a for a in AVATARS if a['id'] == user['avatar_id']), AVATARS[0])
    
    return render_template('dashboard.html', 
                         user=user, 
                         avatars=AVATARS, 
                         current_avatar=current_avatar,
                         wellness_tasks=WELLNESS_TASKS)

@app.route('/complete_task', methods=['POST'])
def complete_task():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    task_id = request.json.get('task_id') or 1
    duration = request.json.get('duration') or 0
    
    user = session['user']
    # New point system: 2 points per minute
    points_earned = duration * 2
    user['points'] += points_earned
    user['total_wellness_time'] += duration
    
    # Track task completion
    task_key = f"task_{task_id}"
    if task_key not in user['task_completions']:
        user['task_completions'][task_key] = 0
    user['task_completions'][task_key] += 1
    
    session['user'] = user
    
    return jsonify({
        'success': True, 
        'points': user['points'],
        'points_earned': points_earned,
        'total_wellness_time': user['total_wellness_time']
    })

@app.route('/complete_study', methods=['POST'])
def complete_study():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    duration = request.json.get('duration') or 0
    
    user = session['user']
    user['points'] += 10
    user['study_sessions'] += 1
    
    session['user'] = user
    
    return jsonify({'success': True, 'points': user['points']})

@app.route('/stop_study', methods=['POST'])
def stop_study():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = session['user']
    # Subtract 5 points for stopping early
    user['points'] = max(0, user['points'] - 5)
    
    session['user'] = user
    
    return jsonify({'success': True, 'points': user['points']})

@app.route('/update_most_used_app', methods=['POST'])
def update_most_used_app():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    app_name = request.json.get('app_name') or ''
    
    user = session['user']
    user['most_used_app'] = app_name
    
    # Bonus points if they select this wellness app
    if app_name.lower() in ['wellness app', 'this app', 'this one']:
        user['points'] += 20
    
    session['user'] = user
    
    return jsonify({'success': True, 'points': user['points']})

@app.route('/change_avatar', methods=['POST'])
def change_avatar():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    avatar_id = request.json.get('avatar_id') or 1
    
    user = session['user']
    
    # Check if avatar is unlocked
    if avatar_id in user.get('unlocked_avatars', []):
        user['avatar_id'] = avatar_id
        session['user'] = user
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Avatar not unlocked'}), 400
