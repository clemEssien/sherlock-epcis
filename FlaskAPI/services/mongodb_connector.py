class MongoDBConnector():

    def __init__(self, collection) -> None:
        self._collection = collection

    @property
    def collection(self) -> object:
        return self._collection

    def get(self, **kargs):
        try:
            result = self._collection.objects.get(**kargs)
        except Exception:
            raise LookupError()

        return result

    def update(self, obj, **kargs):
        obj.update(**kargs)