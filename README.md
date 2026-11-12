# GuliDesign — gulidesign.uz
## Backend (Django REST Framework)
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations api && python manage.py migrate
python manage.py createsuperuser && python manage.py runserver
Admin panel: http://localhost:8000/admin/  (mahsulot, kategoriya, buyurtma, blog, xabarlar, sayt kontaktlari/sozlamalari)
## Frontend (React + Vite)
cd frontend && npm install && npm run dev      # build: npm run build -> dist/
## Deploy (gulidesign.uz)
gunicorn config.wsgi + nginx: / -> frontend/dist, /api, /admin, /media -> gunicorn. SECRET_KEY, DEBUG=0, PostgreSQL, certbot (HTTPS).
