# Installation

## Build and run
```bash
docker-compose up
```

## Api endpoint for conversion using link
```bash
curl -X POST -H 'Content-Type: application/json' -i http://localhost:8000/v1/convert_html_to_pdf/link/ --data '{"url": "https://www.djangoproject.com/"}'
```

## Api endpoint for conversion using data
```bash
curl -X POST \
  -i http://localhost:8000/v1/convert_html_to_pdf/data/ \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F html_file=@yandex.html
```