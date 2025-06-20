import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-gg74fs%$^&xgs1#bxc3r9^tyerp+kn)6=n8ez!tq^1#fjw3')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']  # Adjust for production

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Local apps
    'doctors',
    'apps.users',
    'apps.chatbot',
    'apps.appointments_api',
    'appointments',
    'oauth_integration',  # Make sure this is here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add after MIDDLEWARE
SITE_ID = 1

ROOT_URLCONF = 'gynecology_chatbot_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gynecology_chatbot_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Custom authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'allauth.socialaccount.auth_backends.SocialAccountBackend',
]

# Login/Logout URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# Email settings (for now, use console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# JWT will use email as username
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only
# For production, specify allowed origins:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

# API Keys for LLM services
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GROK_API_KEY = os.environ.get('GROK_API_KEY', '')

# LLM Model Configuration
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
GROK_MODEL = os.environ.get('GROK_MODEL', 'grok-2')

# System Prompt for Gynecology Chatbot
GYNECOLOGY_SYSTEM_PROMPT = """
You are a virtual gynecology assistant providing supportive, concise guidance for gynecological concerns. Your responses must be brief yet impactful. In every response:
Be Concise and Direct: Keep responses short and focused. Get straight to the essential information without unnecessary elaboration. Aim for clarity in fewer words.
Lead with Key Information: Start with the most important point first. Prioritize what the user needs to know most urgently.
Provide Targeted Reassurance: When symptoms are likely benign, state this clearly and early in your response to ease anxiety quickly.
Essential Professional Guidance: Always include a brief but clear recommendation to consult a healthcare provider. Make this guidance prominent but concise.
No Diagnoses: You inform and support, never diagnose. Keep medical boundaries clear in minimal words.
Empathetic but Efficient: Maintain warmth and understanding while being economical with words. Every sentence should serve a purpose.
Focus on Action: When possible, guide users toward practical next steps rather than extensive explanations.
Professional Simplicity: Use accessible language that conveys medical professionalism without complexity or jargon.
Remember: Impact over length. Make every word count. Be the caring, knowledgeable voice that gets to the heart of what matters most.
and dont use the term visit docotor to often as it doesnt sound natural like a dctor would say.
"""

# Google Cloud Firestore Configuration
GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT', 'gynecology-chatbot-fresh-2025')
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(BASE_DIR, 'firestore-key.json')

# Database Selection Mode
USE_FIRESTORE = os.environ.get('USE_FIRESTORE', 'False') == 'True'

# Firestore settings
FIRESTORE_SETTINGS = {
    'project_id': GOOGLE_CLOUD_PROJECT,
    'credentials_path': GOOGLE_APPLICATION_CREDENTIALS,
    'collections': {
        'users': 'users',
        'conversations': 'conversations', 
        'messages': 'messages',
        'doctors': 'doctors',
        'appointments': 'appointments',
        'patient_queries': 'patient_queries',
    }
}

# Add logging for Firestore operations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'firestore.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'firestore': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# Google OAuth Configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# OAuth Session Configuration
SOCIALACCOUNT_SESSION_COOKIE_AGE = 5 * 24 * 60 * 60  # 5 days in seconds

# NEW: Updated OAuth settings (replace the old deprecated ones)
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_LOGIN_METHODS = ['email']  # NEW: replaces ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # NEW: replaces EMAIL_REQUIRED and USERNAME_REQUIRED
SOCIALACCOUNT_QUERY_EMAIL = True

# Google OAuth Credentials
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '')

# OAuth redirect URLs
OAUTH_REDIRECT_URI = 'http://localhost:8001/auth/callback/'
OAUTH_SUCCESS_URL = 'http://localhost:8001/'


# # OAuth Session Configuration
# SOCIALACCOUNT_SESSION_COOKIE_AGE = 5 * 24 * 60 * 60  # 5 days in seconds

# # OAuth Auto-signup settings
# SOCIALACCOUNT_AUTO_SIGNUP = True
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# SOCIALACCOUNT_QUERY_EMAIL = True

# # Google OAuth Credentials (add to your .env file)
# GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '')
# GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '')

# # OAuth redirect URLs
# OAUTH_REDIRECT_URI = 'http://localhost:8001/auth/callback/'
# OAUTH_SUCCESS_URL = 'http://localhost:8001/'