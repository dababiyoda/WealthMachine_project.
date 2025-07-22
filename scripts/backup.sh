#!/bin/bash
# Backup script for knowledge graph and relational database.
set -euo pipefail

DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backups/${DATE}"
mkdir -p "$BACKUP_DIR"

# Backup Neo4j database (requires neo4j-admin tool)
if command -v neo4j-admin &> /dev/null; then
    echo "Backing up Neo4j database..."
    neo4j-admin dump --database=neo4j --to="${BACKUP_DIR}/neo4j.dump"
fi

# Backup Postgres database using pg_dump (requires DATABASE_URL env)
if [ -n "${DATABASE_URL:-}" ]; then
    echo "Backing up Postgres database..."
    pg_dump "$DATABASE_URL" > "${BACKUP_DIR}/postgres.sql"
fi

echo "Backups stored in ${BACKUP_DIR}"
