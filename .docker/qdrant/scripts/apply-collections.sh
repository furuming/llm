#!/bin/sh
set -eu

QDRANT_URL="${QDRANT_URL:-http://vdb:6333}"

echo "Waiting for Qdrant at ${QDRANT_URL}..."
until curl -fsS "${QDRANT_URL}/readyz" >/dev/null; do
  sleep 1
done

for definition in /collections/*.json; do
  [ -e "${definition}" ] || continue

  collection_name="$(basename "${definition}" .json)"
  status_code="$(
    curl -s -o /dev/null -w '%{http_code}' \
      "${QDRANT_URL}/collections/${collection_name}" || true
  )"

  if [ "${status_code}" = "200" ]; then
    echo "Collection '${collection_name}' already exists"
    continue
  fi

  if [ "${status_code}" != "404" ]; then
    echo "Failed to inspect collection '${collection_name}' (HTTP ${status_code})" >&2
    exit 1
  fi

  echo "Creating collection '${collection_name}'"
  curl -fsS -X PUT "${QDRANT_URL}/collections/${collection_name}" \
    -H 'Content-Type: application/json' \
    --data-binary @"${definition}"
done
