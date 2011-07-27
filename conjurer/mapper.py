
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
        if row is None:
            return None

        obj = self.target_class()
        for mapping in self.mappings:
            (column, attr_name, transform) = mapping
            row_value = row[column]
            if row_value is not None:
                attr_value = transform.to_object_attr(row_value)
            else:
                attr_value = None
            setattr(obj, attr_name, attr_value)
        return obj

    def result_to_object_iter(self, result):
        for row in result:
            yield self._object_from_row(row)

    def result_to_object(self, result):
        row = result.fetchone()
        return self._object_from_row(row)

    def insert_stmt_from_object(self, obj, exclude_attrs=None):
        if exclude_attrs:
            # we ask for an iterable but really
            # we want a dict so we can check it
            # quickly.
            _exclude_attrs = exclude_attrs
            exclude_attrs = {}
            for attr_name in _exclude_attrs:
                exclude_attrs[attr_name] = True
            # Don't need this anymore
            del _exclude_attrs

        insert_args = {}

        for mapping in self.mappings:
            (column, attr_name, transform) = mapping
            attr_value = getattr(obj, attr_name, None)
            if attr_value is not None:
                insert_value = transform.from_object_attr(attr_value)
            else:
                insert_value = None
            insert_args[column.name] = insert_value

        insert = self.source_table.insert()
        return insert.values(**insert_args)


    def update_stmt_from_object(self, obj):
        pass

