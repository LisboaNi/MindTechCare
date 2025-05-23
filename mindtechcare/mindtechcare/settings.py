import os
import sys
import pymysql
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
pymysql.install_as_MySQLdb()


DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-^q3!by+2z9h5$o$8vd1j^x@em$1*-cte)inv_t)tk+9b4gea43")
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminDev",
    "accounts",
    "rest_framework",
    "validations",
    "employees",
    "github",
    "trello",
    "dashboard",
    "plan",
    "rest_framework.authtoken",
]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Adiciona o diretório 'src' ao PYTHONPATH para que o Django encontre os apps
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = (
    "smtp.gmail.com" 
)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "itjobs.pim@gmail.com"  
EMAIL_HOST_PASSWORD = "bdkgasbhgbxhxgex"  

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000"]

ROOT_URLCONF = "mindtechcare.urls"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mindtechcare.wsgi.application"

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lumen",
    "dark_mode_theme": None,
}


JAZZMIN_SETTINGS = {
    # Título da janela (será o padrão de current_admin_site.site_title se estiver ausente ou None)
    "site_title": "Library Admin",
    # Título na tela de login (máximo 19 caracteres) (padrão: current_admin_site.site_header)
    "site_header": "Library",
    # Título da marca no canto superior esquerdo (máximo 19 caracteres) (padrão: current_admin_site.site_header)
    "site_brand": "MindTechCare",
    # Logo do site (deve estar nos arquivos estáticos), usado na marca no canto superior esquerdo
    "site_logo": "../static/images/favicon/logowhite.png",
    # Logo usada no formulário de login (padrão: site_logo)
    "login_logo": "../static/images/logo_mindtechcare.png",
    # Logo para formulário de login no tema escuro (padrão: login_logo)
    "login_logo_dark": None,
    # Classes CSS aplicadas à logo acima
    "site_logo_classes": None,
    # Caminho relativo para o favicon do site (padrão: site_logo) (idealmente 32x32 px)
    "site_icon": None,
    # Texto de boas-vindas na tela de login
    "welcome_sign": "Bem-Vindo",
    # Texto de direitos autorais no rodapé
    "copyright": "MindTechCare",
    # Lista de modelos para buscar na barra de pesquisa. Se omitido, a barra de busca é escondida.
    # Pode ser uma lista ou uma string simples (campo de pesquisa único)
    "search_model": ["auth.User", "auth.Group"],
    # Campo do modelo User que contém a imagem/avatar (ImageField/URLField/CharField ou função)
    "user_avatar": None,
    ############
    # Menu Topo #
    ############
    # Links colocados no menu superior
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "auth.User"},
        {"app": "books"},
    ],
    #############
    # Menu Usuário #
    #############
    # Links adicionais no menu do usuário no canto superior direito (não permite tipo "app" na URL)
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "auth.user"},
    ],
    #############
    # Menu Lateral #
    #############
    # Exibir ou não o menu lateral
    "show_sidebar": True,
    # Expande o menu automaticamente
    "navigation_expanded": True,
    # Ocultar estes apps no menu lateral (ex: "auth")
    "hide_apps": [],
    # Ocultar estes modelos no menu lateral (ex: "auth.user")
    "hide_models": [],
    # Ordenar o menu lateral com base nessa lista (não precisa conter todos os apps/modelos)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],
    # Links personalizados agrupados por app
    "custom_links": {
        "books": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fas fa-comments",
                "permissions": ["books.view_book"],
            }
        ]
    },
    # Ícones personalizados para apps/modelos no menu lateral (ver link com lista de ícones FontAwesome)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "authtoken.TokenProxy": "fa-solid fa-key",
        "github.AtividadeGitHub": "fa-brands fa-github",
        "github.RepositorioGitHub": "fa-brands fa-github",
        "trello.BoardTrello": "fa-brands fa-trello",
        "trello.CardTrello": "fa-brands fa-trello",
        "employees.Employee": "fas fa-users",
        "accounts.UserModel": "fas fa-user",
    },
    # Ícone padrão para apps (quando não especificado)
    "default_icon_parents": "fas fa-chevron-circle-right",
    # Ícone padrão para modelos (quando não especificado)
    "default_icon_children": "fas fa-circle",
    #################
    # Modal de Relacionamento #
    #################
    # Usar modais em vez de pop-ups
    "related_modal_active": False,
    #############
    # Ajustes de Interface #
    #############
    # Caminhos relativos para seus CSS/JS customizados (devem estar nos arquivos estáticos)
    "custom_css": "../static/css/custom_admin.css",
    "custom_js": None,
    # Usar fontes do Google Fonts CDN (ou use custom_css para fornecer sua fonte)
    "use_google_fonts_cdn": True,
    # Mostrar o personalizador de UI na barra lateral
    "show_ui_builder": True,
    ###############
    # Tela de Edição #
    ###############
    # Formato da tela de edição: opções possíveis:
    # - single (tudo em um formulário só)
    # - horizontal_tabs (padrão)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # Substituir formato da tela de edição por modelo específico
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Adicionar seletor de idioma no admin
    # "language_chooser": True,
}

INSTALLED_APPS += ['storages']

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Arquivos de mídia (uploads)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

SECURE_SSL_REDIRECT = True # Redireciona HTTP para HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'