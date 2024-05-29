from flask import request, jsonify, render_template, redirect, url_for
from app import app, db
from models import URL
import validators
import string
import random

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_url = generate_short_url()
    new_url = URL(original_url=original_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'original_url': original_url, 'short_url': short_url}), 201

@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()

    return redirect(url.original_url)

@app.route('/urls', methods=['GET'])
def get_all_urls():
    urls = URL.query.all()
    return jsonify([{'original_url': url.original_url, 'short_url': url.short_url} for url in urls])

@app.route('/')
def index():
    return render_template('index.html')
