# Messstellenbetreiberportal API

## Authorization
### Header
```json
{
  "Authorization": Bearer token  
}
```
Token must be signed with HS256 and should contain the object `JwtToken`.

## Endpoints

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

## Objects

### JwtToken
Id is the stromzaehler-id  
Mode is the used hash algorithm for the signature. Should be sha256.  
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