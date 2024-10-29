# The cheapest products!

## How To

`pyenv virtualenv 3.1.1 cheapest-shit
pyenv local cheapest-shit`

Next

`pip install -r requirements.txt -r requirements-dev.txt`

Run
`Make all`

## Update Dependencies with pip-tools

`pip-compile requirements.in
pip-compile requirements-dev.in
pip install -r requirements.txt -r requirements-dev.txt
`
