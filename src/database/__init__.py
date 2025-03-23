import pymongo


class Inventory:
    def __init__(self, shopping_list: pymongo.database.Database):
        self.sl = shopping_list["items"]

    def if_exists(self, item_name: str) -> bool:
        return bool(self.sl.find_one({"name": item_name}))

    def if_exists_id(self, id: int) -> bool:
        return bool(self.sl.find_one({"_id": id}))

    def assign_sno(self, id: int = None) -> int:
        if id is not None:
            return id
        return self.sl.count_documents({}) + 1

    def set_qty(self, item_name, old_qty: int = None) -> int:
        qty = self.sl.find_one({"name": item_name})["qty"] + 1
        if old_qty != None:
            qty = old_qty
        return qty

    def update_item(
        self,
        id: int,
        item_name: str = None,
        qty: int = None,
        item_category: int = None,
        item_price: int = None,
        reorder_level: int = None,
    ):
        update_fields = {}
        if item_name is not None:
            update_fields["name"] = item_name
        if qty is not None:
            update_fields["qty"] = qty
        if item_category is not None:
            update_fields["category"] = item_category
        if item_price is not None:
            update_fields["price"] = item_price
        if reorder_level is not None:
            update_fields["rl"] = reorder_level

        if update_fields:
            self.sl.update_one({"_id": id}, {"$set": update_fields})

    def add_item(
        self,
        item_name: str,
        qty: int,
        item_category: str,
        item_price: int,
        reorder_level: int,
    ):
        if not self.if_exists(item_name):
            self.sl.insert_one(
                {
                    "_id": self.assign_sno(),
                    "name": item_name,
                    "category": item_category,
                    "qty": qty,
                    "price": item_price,
                    "rl": reorder_level,
                }
            )
        else:
            print("Item Exists")

    def del_item(self, id: int):
        if self.if_exists_id(id):
           self.sl.delete_one({"_id": id})
        else:
            print("Not Found")

    def order_item(self, id: int, qty: int):
        if self.if_exists_id(id):
            new_qty = self.sl.find_one({"_id": id})["qty"] - qty
            if new_qty < 0:
                return
            else:
                self.sl.update_one({"_id": id}, {"$set": {"qty": new_qty}})

    def show(self):
        for x in self.sl.find():
            print(x)
    
    def set_login_status(stat: bool):
        print("Failed Setting Login status")

    def get_login_status() -> bool:
        return True

    def fetch_all(self):
        lst = []
        for x in self.sl.find():
            lst.append(
                {
                    "id": x["_id"],
                    "name": x["name"],
                    "category": x["category"],
                    "quantity": x["qty"],
                    "price": x["price"],
                    "reorderLevel": x["rl"],
                }
            )
        return lst
