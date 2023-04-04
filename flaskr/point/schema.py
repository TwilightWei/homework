add_schema = {
    "type" : "object",
    "properties" : {
        "amount" : {"type" : "number"}
    }
}

redeem_schema = {
    "type" : "object",
    "properties" : {
        "commodities" : {
            "type": "array",
            "items": {
                "commodity_id" : {"type" : "number"},
                "amount" : {"type" : "number"}
            }
        }
    }
}