db.createCollection("company", {
    "validator": {
        $jsonSchema: {
            "bsonType": "object",
            "properties": {
                "_id": { "bsonType": "string" },
                "dname": { "bsonType": "string" },
                "manager": { "bsonType": "string" },
                "msdate": {
                    "bsonType": "string",
                    "pattern": "[0-9]{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])"
                },
                "location": {
                    "bsonType": "array",
                    "items": { "bsonType": "string" },
                    "minItems": 1
                },
                "employee": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "e#": {
                                "bsonType": "string",
                            },
                            "name": {
                                "bsonType": "string"
                            },
                            "dob": {
                                "bsonType": "string",
                                "pattern": "[0-9]{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])"
                            },
                            "supervisor": {
                                "bsonType": "string",
                            }
                        },
                        "required": ["e#", "name", "dob"]
                    },
                    "minItems": 1
                }
            },
            "required": ["_id", "dname", "manager", "location", "employee"],
            "additionalProperties": false
        }
    }
});

//pass the validation
db.getCollection("company").insert({
    "_id": "Product Development Department",
    "dname": "Product Development Department",
    "manager": "Eugene N. Betts",
    "msdate": '2013-12-12',
    "location": ["Atlanta", "Portland"],
    "employee": [
        {
            "e#": "AE798",
            "name": "Connie N. Seager",
            "dob": '1984-01-05',
        },
        {
            "e#": "TX987",
            "name": "Lynn J. Skinner",
            "dob": '1992-10-06',
            "supervisor": "AE798"
        }
    ]
});

//fail validation of msdate format
db.getCollection("company").insert({
    "_id": "Business Department",
    "dname": "Business Department",
    "manager": "Kenneth J. Willis",
    "msdate": '2015-13-09',
    "location": ["New York", "Albany"],
    "employee": [
        {
            "e#": "YH391",
            "name": "Gregory M. Platt",
            "dob": '1972-03-05',
        },
        {
            "e#": "TI867",
            "name": "Richard J. Reed",
            "dob": '1992-12-04',
            "supervisor": "YH391"
        },
        {
            "e#": "TI867",
            "name": "Pat R. Mejia",
            "dob": '1987-12-01',
            "supervisor": "YH391"
        }
    ]
});