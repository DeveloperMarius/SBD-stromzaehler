# Messstellenbetreiberportal API

## Authorization
### Header
```json
{
  "Authorization": Bearer token  
}
```
Token must be signed with EdDSA (Ed25519) using the provided private key and should contain the object `JwtToken`.

## Endpoints

### /api/landlord
pass address and get landlord

### /api/stromzaehler
pass address get 

- aktuelle messwerte
- preis pro kwh + history (von bis)
- stromzahler registrieren

### GET /api/healthcheck
Der Endpunkt dient zum Überprüfen, ob das Messstellenbetreiberportal online und
erreichbar ist.

Expected status code: 200

### POST /api/stromzaehler/update
Dieser Endpunkt wird vom Stromzähler genutzt, um den aktuellen Stromzählerstand
zu senden.

#### Request
```json
{
  "readings": Reading[], 
  "logs": LogEntry[]
}
```

### GET /api/stromzaehler/history
Dieser Endpunkt wird vom Kundenportal genutzt, um die Zählerstände von einem Stromzähler in einem bestimmten Zeitraum abzufragen.
#### Request
```json
{
  "stromzaehler-id": 1,
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```
#### Response
```json
{
  "readings": [
    {
      "stromzaehler_id": 1,
      "timestamp": 1701689349628,
      "value": 1234
    }
  ]
}
```

## Objects

### JwtToken
Id is the stromzaehler-id  
Mode is the used hash algorithm for the signature. Should be `SHA256`.  
Signature is the hash of the request body as hex integer
```json
{
  "id": Integer,
  "mode": String,
  "signature": Integer
}
```

### Reading
Timestamp is unix milliseconds timestamp.  
Value is the `zaehlerstand * 100`
```json
{
  "id": Integer,
  "timestamp": Integer,
  "value": Integer
}
```

### LogEntry
Timestamp is unix milliseconds timestamp.
```json
{
  "id": Integer,
  "timestamp": Integer,
  "message": String
}
```