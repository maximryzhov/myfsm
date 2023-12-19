class DotPath:
    @staticmethod
    def get_value(obj, path):
        for key in path.split('.'):
            if key.isdigit():
                key = int(key)
            obj = obj[key]
        return obj

    @staticmethod
    def set_value(obj, path, val):

        def _set_value(obj, path, val):
            first, sep, rest = path.partition(".")
            if first.isdigit():
                first = int(first)
            if rest:
                new_obj = obj[first]
                _set_value(new_obj, rest, val)
            else:
                obj[first] = val
                
        _set_value(obj, path, val)