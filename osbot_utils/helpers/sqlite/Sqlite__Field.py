import inspect
import typing
from decimal import Decimal
from enum import auto, Enum
from typing import Optional, Union

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type


class Sqlite__Field(Kwargs_To_Self):
    cid              : int
    name             : str
    type             : Sqlite__Field__Type
    notnull          : bool
    dflt_value       : Optional[Union[int, str, float, bytes]]
    pk               : bool
    autoincrement    : bool
    unique           : bool
    is_foreign_key   : bool                                                 # Indicates if the field is a foreign key
    references_table : Optional[str]                                        # The table the foreign key references
    references_column: Optional[str]                                        # The column in the referenced table
    on_delete_action : Optional[str]                                        # Action on delete (e.g., CASCADE, SET NULL)
    precision        : Optional[int]                                        # Precision for decimal types
    scale            : Optional[int]                                        # Scale for decimal types
    check_constraint : Optional[str]                                        # Check constraint expression

    def text_for_create_table(self):
        parts = [self.name]  # Start with name

        if self.type == Sqlite__Field__Type.DECIMAL and self.precision is not None and self.scale is not None:
            parts.append(f"DECIMAL({self.precision}, {self.scale})")
        else:
            parts.append(self.type.name)
        if self.pk:
            parts.append("PRIMARY KEY")
            if self.autoincrement:
                parts.append("AUTOINCREMENT")
        if self.unique:
            parts.append("UNIQUE")
        if self.notnull:
            parts.append("NOT NULL")


        if self.check_constraint:
            parts.append(f"CHECK ({self.check_constraint})")

        if self.is_foreign_key and self.references_table and self.references_column:
            fk_constraint = f"FOREIGN KEY ({self.name}) REFERENCES {self.references_table} ({self.references_column})"
            if self.on_delete_action:
                fk_constraint += f" ON DELETE {self.on_delete_action}"
            return fk_constraint

        return " ".join(parts)

    @classmethod
    def fix_from_json_data(cls, json_data):
        if type(json_data) is dict:
            type_type = json_data.get('type')
            mapped_type = Sqlite__Field__Type.type_map().get(type_type)
            if mapped_type:
                json_data['type'] = mapped_type
                return mapped_type


    @classmethod
    def from_json(cls, json_data):
        cls.fix_from_json_data(json_data)
        return super(Sqlite__Field, cls).from_json(json_data)

