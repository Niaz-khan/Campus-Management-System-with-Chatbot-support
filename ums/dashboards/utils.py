from django.utils import timezone
from decimal import Decimal

def try_import(path):
    """Safely import a model/class by dotted path. Return None on failure."""
    try:
        module_path, name = path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[name])
        return getattr(module, name)
    except Exception:
        return None
