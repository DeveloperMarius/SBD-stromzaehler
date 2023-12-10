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

## Asymmetric use of jwts
### Generate key pair
```bash
ssh-keygen -t rsa -b 4096
```
Please specify .ssh/id_rsa as file for saving the key pair 

### Using keys
#### Endcoding
```python3
from cryptography.hazmat.primitives import serialization
import jwt

with open('.ssh/id_rsa', 'r') as file:
    key = file.read()
private_key = serialization.load_ssh_private_key((key.encode()), password=b'')

jwt_token = 'Bearer ' + jwt.encode(jwt_data, private_key, "RS256")
```
#### Decoding
```python3
from cryptography.hazmat.primitives import serialization
import jwt
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2RlIjoiU0hBMjU2Iiwic2lnbmF0dXJlIjoiOWYwYTcyYjJlNDJlZjM3OGUzYjk4ZWFjNTg2ZDMxOGZmOWZkZjI3YmQ5MTNmNTg5M2E0ZTBhZGI2NjhkMWY0OSJ9.pv83FFlEB4qjh9th2UId6qn7Ser-fvmfG4o9IbmkZvYshahagz8GjHkIsph3r8FpdtvENQ5qY_R0_CIfkAdt1q_9KB3B8PlRpKtX4jE4i99Ch3AIafw48XHzj1EtPSHlAwYzbUvDNjIReJ9VbXNWn85SqyFmkynuuwgs8M_k6drzdujlgp27xbMGGgnu7vwQWCy9OuBtlJBzZoNgj_WPAshaF2aD1BQtIfyg8YKVeS95wuChJI0n4Vm15bUgiy0M7xamMllEVag7ux9DP8R8b-yhAru2zN-Jt2kGpTHVWqpFQ6p0S00tmyIcErRbkX6KhxJFcPZLtJ-uNfw6MQzQNDFsP2wZqXw8Wby1FypSw1Kb-CVkl5j18qAq7KGyL1UeHQNgEpTuO4j-h3_q6pjxyo3ZYQY2kaj4MZGXDmqzALlruRBf4cliYAJzHKq2rdhPtXpV12rMo3BkDMmaiMTq7HKqJGTo-sYmEc4hw1aQwb8_JW1IXp5ZfqZqTJRnyYiL'

with open('.ssh/id_rsa.pub', 'r') as file:
    public_key = file.read()

key = serialization.load_ssh_public_key(public_key.encode())
data = jwt.decode(jwt=token, key=key, algorithms=['RS256', ])
```