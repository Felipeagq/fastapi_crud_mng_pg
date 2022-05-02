# FastAPI CRUD with mongo and postgres

## Comandos de Alembic:
- alembic init alembic
- alembic current
- alembic revision --autogenerate -m "first m"
- alembic upgrade head ##postgresql
- docker-compose-postgres.yml

## Future Recomendations:
- Dentro de app no tener otro archivo, solo __init__.py y llamar a todas las librerias desde app.[libreria]
- Usar carpeta core:
    - scheme.
    - modelos.
    - Security.
    - settings.