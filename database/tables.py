SCHEMA = {
    "leveling": {
        "columns": {
            "user_id": "BIGINT  NOT NULL",
            "guild_id": "BIGINT NOT NULL",
            "experience": "BIGINT NOT NULL",
            "created_date": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_date": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
        },
        "constraints": [
            "PRIMARY KEY (guild_id, user_id)"
        ]
    },
}