"""Tools for importing and exporting JSON data to/from class object instances"""

from abc import abstractclassmethod, abstractmethod
from enum import Enum, Flag
import functools
import inspect
import datetime
from uuid import UUID


def jsonid(id):
    """Decorator to set the json value name/id for a function or property"""

    def wrapped(fn):
        @functools.wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)

        if wrapped_f.__doc__:
            wrapped_f.__doc__ += "(json_id=%s)" % id
        else:
            wrapped_f.__doc__ = "(json_id=%s)" % id

        wrapped_f.__jsonid__ = id
        return wrapped_f

    return wrapped


def get_jsonid(prop):
    """Get the json_id decorator value for the specified function or property

    Args:
        prop (function | property): The function or property to retrieve a json_id for

    Returns:
        str: The text of the json_id or None
    """

    try:
        if "json_id=" in prop.__doc__:
            docstr = prop.__doc__
            i = docstr.find("json_id=") + 12
            j = docstr.find(")", i)
            return docstr[i:j]

        else:
            return None
    except:
        pass
        return None


def primitive_to_json(value):
    """Returns a json-compatible string or number for the specified primitive value"""
    if isinstance(value, datetime.datetime):
        return value.isoformat("T").replace("+00:00", "") + "Z"
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    elif isinstance(value, datetime.time):
        return value.strftime("%H:%M:%S.%f")
    elif isinstance(value, int) or isinstance(value, float):
        return value
    elif isinstance(value, str):
        return value
    elif isinstance(value, UUID):
        return str(value)


def is_primitive(value) -> bool:
    """
    Returns True if the type is a primitive value

    Primitive values include str, int, float, UUID, datetime, date, and time.
    """
    if isinstance(value, datetime.datetime):
        return True
    elif isinstance(value, datetime.date):
        return True
    elif isinstance(value, datetime.time):
        return True
    elif isinstance(value, int) or isinstance(value, float):
        return True
    elif isinstance(value, str):
        return True
    elif isinstance(value, UUID):
        return True
    else:
        return False


class JSONValueProvider:
    """An abstract class that can be inherited for the class to provide its own JSON serialization scheme."""

    @abstractmethod
    def getvalue(self):
        """Serialize the contents of the class for export to JSON"""
        pass

    @abstractclassmethod
    def newfromvalue(cls, value):
        """Create a new instance of this class from the contents of a dict returned from a JSON call"""
        pass

    @staticmethod
    def setvalue(self, value) -> None:
        """
        Overridable method to populate the contents of an existing object instance with a dict returned from a JSON call

        Note: This method cannot be overridden in Enum or Flag-based classes.

        """
        if issubclass(type(self), Enum) or issubclass(type(self), Flag):
            raise TypeError("'newfromvalue' not supported on Enum and Flag subclasses")
        pass


def map_to_json(obj):
    """Map a class object instance's data attributes into an object that can be JSON encoded for inserting into JSON

    Args:
        obj (Any): The class object to encode

    Returns:
        Any: The data dictionary that can be exported to a JSON string
    """
    if issubclass(type(obj), JSONValueProvider):
        return obj.getvalue()

    elif is_primitive(obj):
        return obj
        # raise TypeError("Cannot serialize a primitive value")

    elif isinstance(obj, dict):

        dictOut = {}
        keys = obj.keys()

        if len(keys):
            for key in keys:

                if is_primitive(obj[key]):
                    dictOut[key] = primitive_to_json(obj[key])
                elif inspect.isclass(type(obj[key])):
                    dictOut[key] = map_to_json(obj[key])
                else:
                    dictOut[key] = str(obj[key])

        return dictOut

    elif isinstance(obj, list):
        arrOut = []

        for val in obj:
            if is_primitive(val):
                arrOut.append(primitive_to_json(val))
            elif inspect.isclass(type(val)):
                arrOut.append(map_to_json(val))
            else:
                arrOut.append(str(val))

        return arrOut

    fb = {}

    objkeys = []

    bases = inspect.getmro(type(obj))

    for t in bases:
        for v in t.__dict__.keys():
            if v[0] == "_":
                continue

            if not hasattr(t, v):
                continue

            clsvar = getattr(t, v)
            fbid = get_jsonid(clsvar)

            if fbid == None:
                continue

            objkeys.append((v, t, fbid))

    resolved = []

    for (v, t, fbid) in objkeys:

        if v in resolved:
            continue

        resolved.append(v)

        if fbid != None:
            instvar = getattr(obj, v)
            if instvar == None:
                continue

            if issubclass(type(instvar), JSONValueProvider):

                res = instvar.getvalue()

                if res != None:
                    fb[fbid] = res

            elif isinstance(instvar, dict):

                dictOut = {}
                for key in instvar:

                    if is_primitive(instvar[key]):
                        res = primitive_to_json(instvar[key])

                        if res != None:
                            dictOut[key] = res

                    elif inspect.isclass(type(instvar[key])):
                        res = map_to_json(instvar[key])

                        if res != None:
                            dictOut[key] = res

                if len(dictOut.keys()):
                    fb[fbid] = dictOut

            elif isinstance(instvar, list):

                arrOut = []

                for val in instvar:
                    if inspect.isclass(type(val)):
                        arrOut.append(map_to_json(val))
                    else:
                        arrOut.append(primitive_to_json(val))

                if len(arrOut):
                    fb[fbid] = arrOut

            elif is_primitive(instvar):

                res = primitive_to_json(instvar)
                if res != None:
                    fb[fbid] = res

            elif inspect.isclass(type(instvar)):
                res = map_to_json(instvar)
                if res != None:
                    fb[fbid] = res

            else:
                if instvar != None:
                    fb[fbid] = str(instvar)

    return fb


def map_from_json(data, obj, types: dict = None):
    """Map data from a data dictionary (as returned from JSON) to a class object instance's data attributes.

    Args:
        data: Any
            The json data to load
        obj: Any
            The class object to load the data in to
        types: dict
            List of sub types used to map properties and create instances

            types has the following structure:
            types = {
                "property_name": {
                     "type": Type, // The Type object of the property
                     "subtypes": {             // A nested dict that follows the format
                        "property_name": {     // of types to specify the type of properties in the
                            "type": Type,      // specified type entry
                            "subtypes": {}
                     }

            }

    """

    if data == None:
        return None

    objkeys = []

    bases = inspect.getmro(type(obj))

    for t in bases:
        for attr in t.__dict__.keys():
            if attr[0] == "_":
                continue

            if not hasattr(t, attr):
                continue

            clsvar = getattr(t, attr)
            fbid = get_jsonid(clsvar)

            if (fbid == None) or (not fbid in data):
                continue

            objkeys.append((attr, t, fbid))

    resolved = []

    for (attr, t, fbid) in objkeys:

        if attr in resolved:
            continue

        resolved.append(attr)

        if not fbid in data or data[fbid] == None:
            continue

        subtypes = None
        cls = None
        objinst = None

        if types != None and attr in types:
            cls = types[attr]["type"]

        instvar = getattr(obj, attr)

        if issubclass(type(instvar), JSONValueProvider):
            cls = type(instvar)
            setattr(obj, attr, cls.newfromvalue(data[fbid]))

        elif isinstance(instvar, datetime.datetime):
            try:
                dstr = data[fbid]
                if not len(dstr):
                    continue

                setattr(
                    obj,
                    attr,
                    datetime.datetime.strptime(dstr, "%Y-%m-%dT%H:%M:%S.%f%z"),
                )

            except:
                try:
                    setattr(
                        obj, attr, datetime.datetime.strptime(data[fbid], "%Y-%m-%d")
                    )
                except:
                    pass

        elif isinstance(instvar, datetime.date):
            try:
                d = datetime.datetime.strptime(data[fbid], "%Y-%m-%d")
                setattr(obj, attr, datetime.date(d.year, d.month, d.day))
            except:
                pass

        elif isinstance(instvar, UUID):
            setattr(obj, attr, UUID(data[fbid]))

        elif isinstance(instvar, list):
            if cls != None:
                arrOut = []

                for val in data[fbid]:
                    objinst = cls()

                    if "subtypes" in types[attr]:
                        subtypes = types[attr]["subtypes"]

                    if subtypes:
                        map_from_json(val, objinst, subtypes)
                    else:
                        map_from_json(val, objinst)

                    arrOut.append(objinst)

                setattr(obj, attr, arrOut)
            else:
                setattr(obj, attr, data[fbid])

            pass
        elif isinstance(instvar, dict):
            if cls != None:
                dictOut = {}
                for val in data[fbid]:
                    objinst = cls()

                    if "subtypes" in types[attr]:
                        subtypes = types[attr]["subtypes"]

                    if subtypes:
                        map_from_json(data[fbid][val], objinst, subtypes)
                    else:
                        map_from_json(data[fbid][val], objinst)

                    dictOut[val] = objinst

                setattr(obj, attr, dictOut)
            else:
                setattr(obj, attr, data[fbid])
            pass
        elif cls != None:

            if issubclass(cls, JSONValueProvider):
                objinst = cls.newfromvalue(data[fbid])

            else:
                if "instance" in types[attr]:
                    objinst = types[attr]["instance"]
                else:
                    objinst = cls()

                if "subtypes" in types[attr]:
                    subtypes = types[attr]["subtypes"]

                if subtypes:
                    map_from_json(data[fbid], objinst, subtypes)
                else:
                    map_from_json(data[fbid], objinst)

            setattr(obj, attr, objinst)

        else:
            setattr(obj, attr, data[fbid])
