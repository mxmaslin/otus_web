from app import app


@app.template_filter('datetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    if value is None:
        return ""
    return value.strftime(format)
