USER_DATA_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"}
    },
    "required" : ["id","email","first_name","last_name","avatar"]

}

LIST_RESOURCE_SCHEMA = {
"type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "year": {"type": "number"},
        "color": {"type": "string"},
        "pantone_value": {"type": "string"}
    },
    "required" : ["id","name","year","color","pantone_value"]
}

CREATED_USER_SCHEMA = {
"type" : "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"},
        "id": {"type": "string"}
    },
    "required" : ["id"]
}

UPDATED_USER_SCHEMA = {
"type" : "object",
    "properties": {
        "name": {"type": "string"},
        "job": {"type": "string"}
    }
}

