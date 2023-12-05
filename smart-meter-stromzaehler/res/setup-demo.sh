#!/bin/sh

# Stromzähler 1
cat > ../src/.env-1 <<EOT
MESSSTELLENBETREIBER_URL=http://host.docker.internal:9001
JWT_SECRET_KEY=zZ6E8ecJ3ufMrhTpBk4RRtgoYMcWKpqyNH4xYUV8MHENsiixBJgPCherFqBPzwws
STROMZAEHLER_ID=1
EOT
