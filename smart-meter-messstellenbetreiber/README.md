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

### GET /api/healthcheck

Endpoint for cheching if Messstellenbetreiberportal is online and reachable.  
Expected status code: 200

### POST /api/stromzaehler/update

Endpoint for sending readings to Messstellenbetreiber. Used by Stromzähler.

#### Request

```json
{
  "readings": Reading[],
  "logs": LogEntry[]
}
```

### GET /api/stromzaehler/history

Endpoint du get readings of a stromzaehler in a period of time. Used by Kundenportal.

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

### POST /api/stromzaehler/register

Endpoint to register a new stromzaehler. Used by Kundenportal.

#### Request

```json
{
  "id": 1,
  "person": {
    "firstname": "Max",
    "lastname": "Mustermann",
    "gender": 1,
    "phone": "+49...",
    "email": "max@mustermann.de"
  },
  "address": {
    "street": "Musterstraße",
    "plz": 12345,
    "city": "Musterstadt",
    "state": "NRW",
    "country": "Germany"
  }
}
```

`"id"` of the stromzaehler to be registered

#### Response

```json
{
  "success": true,
  "stromzaehler_id": 1,
  "owner_id": 2,
  "address_id": 4
}
```

## Objects

### JwtToken

Id is the stromzaehler-id  
Mode is the used hash algorithm for the signature. Should be `SHA256`.  
Signature is the hash of the request body as hex integer.  
Type must be either `"kundenportal"` or `"stromzaehler`"

```json
{
  "type": String,
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
