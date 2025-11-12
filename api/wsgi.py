import os
import sys
import traceback

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maganghub.settings')

# Import and expose the WSGI application; print traceback on failure so Vercel logs show it
try:
    from web.maganghub.wsgi import application
    # Vercel's python runtime expects a variable named `app` for WSGI/ASGI compatibility
    app = application
except Exception:
    traceback.print_exc(file=sys.stderr)
    raise
