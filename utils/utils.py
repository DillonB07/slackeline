def get_user_data(body, type=None):
    if body.get("type") == "block_actions":
        match type:
            case "user_id":
                return body["user"]["id"]
            case _:
                return body["user"]
    else:
        match type:
            case "user_id":
                return body["event"]["user"]
            case _:
                return body["event"]

