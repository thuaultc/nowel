# :santa: Nowel

Nowel creates random pairings of secret santa participants and also sends the corresponding emails.

## Config

Create your config using the YAML template:

```
cp config.yaml.template config.yaml
```

Replace the fields with your corresponding values, and simply run the script!

## Usage

```
pipenv install
pipenv run ./nowel.py
```

You'll get a random cyclic generation of gifters/receivers, followed by a prompt for sending confirmation.
