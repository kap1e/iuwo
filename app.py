from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import markdown

application = Flask(__name__)
application.config['SECRET_KEY'] = 'key'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(application.instance_path, 'database.db')
application.config['SESSION_COOKIE_SECURE'] = False

try:
    os.makedirs(application.instance_path)
except OSError:
    pass
db = SQLAlchemy(application)

from models import User, Progress


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(application)

def load_courses():
    courses = {}
    data_folder = os.path.join(os.path.dirname(__file__), 'courses_data')
    content_folder = os.path.join(os.path.dirname(__file__), 'course_content')
    for filename in os.listdir(data_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                course_data = json.load(f)
                course_name = course_data['name']
                course_slug = course_data.get('slug')
                if not course_slug:
                    course_slug = course_name.lower()
                print(f"Загрузка курса: {course_name} (slug: {course_slug})")
                course_folder = os.path.join(content_folder, course_slug)
                for section in ['history', 'current_usage', 'practice']:
                    content_path = os.path.join(course_folder, f"{section}.md")
                    print(f"Ищем файл контента: {content_path}")
                    if os.path.exists(content_path):
                        with open(content_path, 'r', encoding='utf-8') as content_file:
                            content_raw = content_file.read()
                            content_html = markdown.markdown(content_raw)
                            course_data[section] = content_html
                            print(f"Загружен контент для раздела {section} курса {course_name}")
                    else:
                        course_data[section] = ''
                        print(f"Файл контента для раздела {section} курса {course_name} не найден")
                courses[course_name] = course_data
    return courses

courses_dict = load_courses()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            error = 'Пользователь с таким именем уже существует'
            return render_template('register.html', error=error)
        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            error = 'Неверный логин или пароль'
            return render_template('login.html', error=error)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/')
def index():
    courses = []
    for course_name, course_data in courses_dict.items():
        course_progress = 0
        if current_user.is_authenticated:
            total_tasks = len(course_data['tasks'])
            completed_tasks = Progress.query.filter_by(
                user_id=current_user.id,
                course_name=course_name,
                completed=True
            ).count()
            course_progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
        courses.append({
            'name': course_name,
            'description': course_data['description'],
            'progress': course_progress
        })
    return render_template('index.html', courses=courses)

@application.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

course_sections = ['history', 'current_usage', 'practice']

@application.route('/course/<course_name>/<section>', methods=['GET', 'POST'])
@login_required
def course(course_name, section):
    if section not in course_sections:
        abort(404)

    # Получаем данные курса
    course = courses_dict.get(course_name)
    if not course:
        abort(404)

    current_index = course_sections.index(section)
    prev_section = course_sections[current_index - 1] if current_index > 0 else None
    next_section = course_sections[current_index + 1] if current_index < len(course_sections) - 1 else None

    section_titles = {
        'history': 'История',
        'current_usage': 'Нынешнее применение',
        'practice': 'Практика'
    }

    section_title = section_titles.get(section, 'Раздел')

    if section == 'practice':
        tasks = course['tasks']

        if request.method == 'POST':
            task_id = int(request.form['task_id'])
            submitted_flag = request.form['flag']
            task = next((t for t in tasks if t['id'] == task_id), None)

            if task:
                if submitted_flag == task['flag']:
                    progress = Progress.query.filter_by(
                        user_id=current_user.id,
                        course_name=course_name,
                        task_id=task_id
                    ).first()
                    if not progress:
                        progress = Progress(
                            user_id=current_user.id,
                            course_name=course_name,
                            task_id=task_id,
                            completed=True
                        )
                        db.session.add(progress)
                        db.session.commit()
                    else:
                        if not progress.completed:
                            progress.completed = True
                            db.session.commit()
                    flash('Флаг верный! Задание засчитано.')
                else:
                    flash('Неверный флаг. Попробуйте снова.')
            else:
                flash('Задание не найдено.')

            return redirect(url_for('course', course_name=course_name, section='practice'))

        user_progress = Progress.query.filter_by(
            user_id=current_user.id,
            course_name=course_name
        ).all()
        completed_tasks = [p.task_id for p in user_progress if p.completed]

        return render_template(
            'course_practice.html',
            course_name=course_name,
            tasks=tasks,
            completed_tasks=completed_tasks,
            section=section,
            section_title=section_title,
            prev_section=prev_section,
            next_section=next_section
        )

    else:
        content = course.get(section, '')
        if not content:
            content = "<p>Контент этого раздела еще не добавлен.</p>"

        return render_template(
            'course_section.html',
            course_name=course_name,
            content=content,
            section=section,
            section_title=section_title,
            prev_section=prev_section,
            next_section=next_section
        )


if __name__ == "__main__":
    db.create_all()
    application.run(host='0.0.0.0')