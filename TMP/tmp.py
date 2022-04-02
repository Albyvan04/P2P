import json

filename = "config.json"

jsonObject = {
        "DEFAULT_DB_NAME": "postgres",
        "DB_NAME": "napster",
        "USER": "postgres",
        "PSW": "password",
        "IP": "localhost",
        "PORT": "5432"
    }

with open(filename, "w") as output:
    json.dump(jsonObject, output)