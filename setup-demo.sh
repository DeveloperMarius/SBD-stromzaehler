#!/bin/sh
# Cleanup
rm -rf ./smart-meter-messstellenbetreiber/res/database.db
rm -rf ./smart-meter-stromzaehler/generated
mkdir ./smart-meter-stromzaehler/generated

# Init Messstellenbetreiber DB first
sqlite3 --init ./smart-meter-messstellenbetreiber/res/database.sql ./smart-meter-messstellenbetreiber/res/database.db .quit

# Kundenportal
rm -rf /tmp/key-*
openssl genpkey -algorithm ed25519 -out /tmp/key-private.pem
openssl pkey -in /tmp/key-private.pem -pubout -out /tmp/key-public.pem
public_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-public.pem)
private_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-private.pem)
rm -rf /tmp/key-*
cat > ./smart-meter-kundenportal/.env <<EOT
KUNDENPORTAL_ID=1
SECRET_PUBLIC_KEY=$public_key
SECRET_PRIVATE_KEY=$private_key
EOT
sqlite3 smart-meter-messstellenbetreiber/res/database.db "INSERT INTO kundenportale VALUES (1, 'http://host.docker.internal:9001', '$public_key')"

# Messstellenbetreiber
rm -rf /tmp/key-*
openssl genpkey -algorithm ed25519 -out /tmp/key-private.pem
openssl pkey -in /tmp/key-private.pem -pubout -out /tmp/key-public.pem
public_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-public.pem)
private_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-private.pem)
rm -rf /tmp/key-*
cat > ./smart-meter-messstellenbetreiber/res/.env <<EOT
PUBLIC_KEY=$public_key
PRIVATE_KEY=$private_key
EOT
sqlite3 smart-meter-messstellenbetreiber/res/database.db "INSERT INTO persons VALUES (NULL, 'Gigantikus', 'Maximus', 1, '112', 'max@giga.de')"
sqlite3 smart-meter-messstellenbetreiber/res/database.db "INSERT INTO addresses VALUES (NULL, 'Beispielstraße 1', 60385, 'Frankfurt am Main', 'Hessen', 'Deutschland')"

create_stromzaehler() {
  stromzaehler_id=$1
  sqlite3 --init ./smart-meter-stromzaehler/res/database.sql ./smart-meter-stromzaehler/generated/database-$stromzaehler_id.db .quit
  rm -rf /tmp/key-*
  openssl genpkey -algorithm ed25519 -out /tmp/key-private.pem
  openssl pkey -in /tmp/key-private.pem -pubout -out /tmp/key-public.pem
  public_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-public.pem)
  private_key=$(sed ':a;N;$!ba;s/\n/\\n/g' /tmp/key-private.pem)
  rm -rf /tmp/key-*
  cat > ./smart-meter-stromzaehler/generated/.env-$stromzaehler_id <<EOT
MESSSTELLENBETREIBER_URL=http://host.docker.internal:9001
STROMZAEHLER_ID=$stromzaehler_id
PUBLIC_KEY=$public_key
PRIVATE_KEY=$private_key
EOT
  sqlite3 smart-meter-messstellenbetreiber/res/database.db "INSERT INTO stromzaehler VALUES ($stromzaehler_id, '$public_key', 1, 1, 1)"
}

create_stromzaehler 1
create_stromzaehler 2