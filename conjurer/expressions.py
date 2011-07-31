
from sqlalchemy.sql.operators import ColumnOperators
import sqlalchemy.sql.operators as operators
from sqlalchemy.sql.expression import ClauseElement
from conjurer.transforms import IdentityTransform


class AttributeElement(ColumnOperators):

    def __init__(self, column, transform):
        self.column = column
        if type(transform) is IdentityTransform:
            self.tranform = None
        else:
            self.transform = transform

    def __handle_transform(self, op, obj):
        if self.transform is not None:
            if (op is operators.like_op or
                op is operators.ilike_op or
                op is operators.notlike_op or
                op is operators.notilike_op):
                raise ValueError(
                    "Can't apply LIKE to an attribute with a transform")

            if isinstance(obj, ClauseElement):
                # This comparison probably won't yield anything
                # meaningful unless both sides share exactly
                # the same transform and underlying value,
                # but let's let the caller do it anyway.
                return obj
            else:
                return self.transform.from_object_attr(obj)
        else:
            return obj

    def operate(self, op, obj):
        obj = self.__handle_transform(op, obj)
        return self.column.operate(op, obj)

    def reverse_operate(self, op, obj):
        obj = self.__handle_transform(op, obj)
        return self.column.reverse_operate(op, obj)
