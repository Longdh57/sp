# Alembic Documentation
- Installation
```
$ pip install alembic
```
- Init
```
$ alembic init alembic
```
- Other command
```
$ alembic revision --autogenerate   # auto generate migration
$ alembic upgrade head              # upgrade DB to last migration
$ alembic downgrade -1              # downgrade DB
$ alembic history                   # show migration history
```