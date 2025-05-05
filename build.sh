
set -o errexit

pip install pipenv
pipenv install
pipenv run python -m flask db upgrade

