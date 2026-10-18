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

## Apps

- `venues` — places where events happen
- `events` — concerts / events
- `performers` — artists and bands