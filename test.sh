#!/bin/bash
#
# Run fooder api tests
#

echo "Running fooder api tests"

# if exists, remove test.db
[ -f test.db ] && rm test.db

# create test env values
export DB_URI="sqlite+aiosqlite:///test.db"
export ECHO_SQL=0
export SECRET_KEY=$(openssl rand -hex 32)
export REFRESH_SECRET_KEY=$(openssl rand -hex 32)
export API_KEY=$(openssl rand -hex 32)

python -m fooder --create-tables

# finally run tests
if [[ $# -eq 1 ]]; then
  python -m pytest fooder --disable-warnings -sv -k "${1}"
else
  python -m pytest fooder --disable-warnings -sv
fi

status=$?

# unset test env values
unset POSTGRES_USER
unset POSTGRES_DATABASE
unset POSTGRES_PASSWORD
unset SECRET_KEY
unset REFRESH_SECRET
unset API_KEY

# if exists, remove test.db
[ -f test.db ] && rm test.db

exit $status
