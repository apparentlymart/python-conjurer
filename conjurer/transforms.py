
class BaseTransform(object):
    "Base class for transforms"

    def to_object_attr(self, column_value, row):
        raise Exception("%r must override to_object_attr" % self)

    def from_object_attr(self, attr_value):
        raise Exception("%r must override from_object_attr" % self)


_identity_transform_instance = None
class IdentityTransform(object):
    "A transform that does absolutely nothing. The default."

    @staticmethod
    def instance():
        global _identity_transform_instance
        if _identity_transform_instance is None:
            _identity_transform_instance = IdentityTransform()
        return _identity_transform_instance

    def to_object_attr(self, column_value, row):
        return column_value

    def from_object_attr(self, attr_value):
        return attr_value


# This is really just an example, but maybe it's useful sometimes.
class PaddedHexTransform(object):
    "A transform for integers in the DB that become padded hex strings in the object."

    def __init__(self, size=8):
        self.size = size

    def to_object_attr(self, column_value, row):
        fmt = "%%0%ix" % self.size
        return fmt % column_value

    def from_object_attr(self, attr_value):
        attr_value = str(attr_value)

        # New value should be the right length
        if len(attr_value) != self.size:
            raise ValueError("Attribute value must be %i characters long" % self.size)

        # Will raise ValueError if the value isn't
        # a valid hex string.
        return int(attr_value, 16)

