# Smart Document Extractor 📄🧠

API de extracción documental orientada a portfolio para LinkedIn.

## Stack
- FastAPI + Pydantic
- Pipeline con puertos (`OCREngine`, `LLMEngine`)
- Docker + test E2E

## Endpoints
- `GET /api/health`
- `POST /api/extract` (multipart file)

## Ejecutar
```bash
docker compose up --build
```
API: `http://localhost:8001`
Swagger: `http://localhost:8001/docs`

## Test E2E
```bash
python -m pytest app/tests/test_e2e.py
```

## Ejemplo rápido
```bash
curl -X POST http://localhost:8001/api/extract \
  -F 'file=@sample.txt;type=text/plain'
```
