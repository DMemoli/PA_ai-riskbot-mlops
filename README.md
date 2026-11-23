# FinTech-AI RiskBot — Seguridad y Gestión de Riesgos en MLOps

Proyecto de aplicación académico: servicio FastAPI para consultas de las políticas de crédito de FinTech-AI.

**Estado actual:** etapa inicial. Se incluyen API, políticas, datasets, contrato Pydantic,
controles de seguridad y Docker. `eval.py`, MLflow, Ragas y el workflow de despliegue
se integrarán en las próximas etapas; no se considera aún finalizada la entrega.

## Estructura

```text
main.py
politicas_credito.json
requirements.txt
requirements-test.txt
Dockerfile
.env.example
.gitignore
.dockerignore
eval_data/eval_security.json     # 20 casos

eval_data/eval_functional.json   # 20 casos
tests/test_contrato.py           # tests sin llamadas a Gemini
README.md
```

## Preparación (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Reemplazar `GEMINI_API_KEY` de `.env` por la clave real. No publicar ese archivo.

Iniciar API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Abrir `http://127.0.0.1:8000/docs` o `http://127.0.0.1:8000/`.

Ejemplo de cuerpo para `POST /inferencia`:

```json
{"prompt": "Cual es la edad minima para una hipoteca", "model": "gemini-3.5-flash-lite"}
```

El campo `model` es opcional y solo admite identificadores configurados en
`GEMINI_ALLOWED_MODELS`. La salida exitosa conserva la forma `{"resultado": "..."}`.

## Tests deterministas iniciales

```powershell
.\.venv\Scripts\python.exe -m pip install pytest httpx
.\.venv\Scripts\python.exe -m pytest -q
```

Estos tests comprueban Pydantic, datasets y fuente JSON sin llamar a Gemini.
No verifican todavía la eficacia real del LLM-Judge.

## Docker

```powershell
docker build -t fintech-riskbot .
docker run --rm -p 8000:8000 --env-file .env fintech-riskbot
```

La imagen usa Python 3.11 y usuario sin privilegios. El archivo `.env` debe quedar local.

## Seguridad y límites

- Las políticas JSON son un escenario ficticio académico, no normativa de crédito aplicable.
- El modelo **no aprueba créditos**; solo responde consultas de políticas.
- Validación estructural no equivale a protección completa contra prompt injection.
- El juez semántico clasifica solicitudes; si Gemini falla, el sistema devuelve HTTP 503/502,
  no un falso HTTP 403 por ataque detectado.
- El servicio solo está preparado como laboratorio: faltan autenticación, control de acceso,
  monitoreo y otras medidas propias de producción real.
- Errores 429/503 del proveedor requieren reintentos con pausas en el futuro `eval.py`.

## Próximas etapas

1. Comprobar la API en local con una consulta válida, una entrada inválida y un ataque.
2. Implementar `eval.py` con MLflow, Ragas y gestión de cuota del proveedor.
3. Configurar GitHub Actions con umbrales de seguridad y relevancia.
4. Configurar Render con Deploy Hook y Auto-Deploy desactivado; después demostrar
   una ejecución verde y una roja.
