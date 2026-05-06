PET_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "status"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["available", "pending", "sold"]},
        "photoUrls": {
            "type": "array",
            "items": {"type": "string"},
        },
        "category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        },
    },
    "additionalProperties": True,
}
