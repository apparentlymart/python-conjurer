
from conjurer.transforms import IdentityTransform


class Mapper(object):

    def __init__(self, source_table, target_class, custom_mappings=None):
        self.target_class = target_class
        self.source_table = source_table
        self.mappings = []

        if custom_mappings is None:
            custom_mappings = {}

        for column in source_table.columns:
            transform = None
            attr_name = None

            if column in custom_mappings:
                target = custom_mappings[column]
                if target is not None:
                    target = tuple(target)
                    attr_name = target[0]
                    if len(target) > 1:
                        transform = target[1]
                else:
                    # Caller can explicitly map to None
                    # to suppress a column from being
                    # mapped at all.
                    continue

            if transform is None:
                transform = IdentityTransform.instance()
            if attr_name is None:
                attr_name = column.name

            self.mappings.append((column, attr_name, transform))

    def _object_from_row(self, row):
        obj = self.target_class()
        for mapping in self.mappings:
            (column, attr_name, transform) = mapping
            setattr(obj, attr_name, transform.to_object_attr(row[column]))
        return obj

    def result_to_object_iter(self, result):
        for row in result:
            yield self._object_from_row(row)

    def result_to_object(self, result):
        row = result.fetchone()
        return self._object_from_row(row)

    def insert_from_object_iter(self, iter):
        pass

    def insert_from_object(self, obj):
        pass

    def update_from_object(self, obj):
        pass

