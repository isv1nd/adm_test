# Installation

* Create virtualenv
```bash
virtualenv .venv -p python3.6
. .venv/bin/activate
```

* Install requirements
```bash
pip install -r requirements/service-requirements.txt
```

* Run migrations
```bash
python manage.py migrate
```

* Run development server
```bash
python manage.py runserver 0.0.0.0:8000
```

* Api endpoint for conversion using link
```bash
curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/v1/convert_html_to_pdf/link/ --data '{"url": "https://www.djangoproject.com/"}'
```

* Api endpoint for conversion using data
```bash
curl -X POST \
  -i http://localhost:8000/v1/convert_html_to_pdf/data/ \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F html_file=@yandex.html
```