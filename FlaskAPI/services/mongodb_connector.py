class MongoDBConnector(): #TODO: create, get_many, get_some, etc.

    def __init__(self, collection) -> None:
        self._collection = collection

    @property
    def collection(self) -> object:
        return self._collection

    def create_one(self, **kargs):
        obj = self._collection(**kargs)
        obj.save()

    def get_one(self, **kargs):
        try:
            result = self._collection.objects.get(**kargs)
        except Exception as e:
            raise e

        return result

    def update(self, obj, **kargs):
        obj.update(**kargs)

    def delete_one(self, **kargs):
        obj = self.get_one(**kargs)
        obj.delete()
    
    def delete_all(self):
        for obj in self._collection.objects:
            obj.delete()