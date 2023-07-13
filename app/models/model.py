from config.db import DB


class UserModel(DB):
    def object(item):
        return {
            "_id": str(item.get('_id')),
            "name": item.get("name"),
            "email": item.get("email"),
            "password": item.get("password"),
            "amount": item.get("amount"),
        }