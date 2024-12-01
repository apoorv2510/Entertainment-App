from flask import flash

def flash_message(message, category='info'):
    """Display a flash message."""
    flash(message, category)
