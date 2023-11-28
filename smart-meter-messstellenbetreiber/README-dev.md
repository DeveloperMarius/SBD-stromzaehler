# Dev Readme

## Database
ORM-Docs: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
### Insert
Insert one
```python
log_instance = StromzaehlerLog(
    stromzaehler=1,
    source_id=1,
    timestamp=1,
    message="Hallo"
)
Variables.get_database().session.add(log_instance)
Variables.get_database().session.commit()
```

Insert multiple
```python
log_instances = [
    StromzaehlerLog(
        stromzaehler=1,
        source_id=1,
        timestamp=1,
        message="Hallo"
    )
]
Variables.get_database().session.add_all(log_instances)
Variables.get_database().session.commit()
```

### Select

Select one
```python
from sqlalchemy import select

statement = select(StromzaehlerLog)
data = Variables.get_database().session.scalar(statement)
```
`data` will be a `StromzaehlerLog`

Select multiple
```python
from sqlalchemy import select

statement = select(StromzaehlerLog)
response = Variables.get_database().session.scalars(statement)
data = response.fetchall()
```

`data` will be a list of `StromzaehlerLog`
