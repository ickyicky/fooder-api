#!/bin/bash
#
# Run fooder api tests
#

set -e

TESTS='test'
[[ $# -eq 1 ]] && TESTS=${1}

echo "Running fooder api tests"

# up containers
DC='docker-compose -f docker-compose.test.yml'

if [ "$(${DC} ps | grep -E 'running|Up' | wc -l)" -gt 0 ]; then
  # down containers to assure a clean database
  echo "stopping containers..."
  ${DC} down --remove-orphans
fi

# create test env values
export POSTGRES_USER=fooder_test
export POSTGRES_DATABASE=fooder_test
export POSTGRES_PASSWORD=$(pwgen 13 1)
export SECRET_KEY=$(openssl rand -hex 32)
export REFRESH_SECRET=$(openssl rand -hex 32)

rm -f .env.test
envsubst < env.template > .env.test

unset POSTGRES_USER
unset POSTGRES_DATABASE
unset POSTGRES_PASSWORD
unset SECRET_KEY
unset REFRESH_SECRET

echo "starting containers..."
${DC} up -d

# Wait for the containers to start
echo "waiting for containers to start..."
while [ "$(${DC} ps | grep -E 'running|Up'  | wc -l)" -lt 2 ]; do
  sleep 1
done

while [ "$(${DC} logs database | grep -E 'database system is ready to accept connections'  | wc -l)" -lt 2 ]; do
  sleep 1
done

# create tables
echo "creating tables..."
${DC} exec api bash -c "python -m fooder --create-tables"

# finally run tests
set -xe
pytest fooder -sv -k "${TESTS}"

# clean up after tests
echo "cleaning up..."
${DC} down --remove-orphans
rm -f .env.test
