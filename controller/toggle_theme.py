from flask import request, redirect, url_for, Blueprint, session

theme_bp = Blueprint("theme", __name__)

@theme_bp.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    back_url = request.referrer or url_for('page.page', page='home') 
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'
    session['theme'] = new_theme 
    
    return redirect(back_url)