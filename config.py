import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.getenv('SECRET_KEY_FLASK')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = os.getenv('DEBUG', False)
REMEMBER_COOKIE_DURATION = 86400  # 1 day

# Flask-Mail SMTP server settings
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.zoho.com')
MAIL_PORT = os.getenv('MAIL_PORT', 587)
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = MAIL_USERNAME