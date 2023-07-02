

def UserModel(item):
    return {
        "_id": str(item['_id']),
        "name": item.get("name"),
        "email": item.get("email"),
        "password": item.get("password"),
    }