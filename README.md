# LocalStage

Catalogue of local concerts and events - venues, performers and events.

## Setup

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | built-in dev key | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts |

The app runs without setting any env vars.

## Test custom 404

```bash
DEBUG=False python manage.py runserver --insecure
```

Open a missing URL, for example http://127.0.0.1:8000/missing-page/

## Apps

- `venues` — places where events happen
- `events` — concerts / events
- `performers` — artists and bands