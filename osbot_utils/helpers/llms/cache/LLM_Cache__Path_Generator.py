from datetime                                                                     import datetime
from typing                                                                       import List, Optional
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                 import Safe_Id
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                    import type_safe


class LLM_Cache__Path_Generator(Type_Safe):
    @type_safe
    def generate_path(self, year     : Optional[int] = None,        # Time components - all optional and independent
                            month    : Optional[int] = None,
                            day      : Optional[int] = None,
                            hour     : Optional[int] = None,
                            domains  : List[Safe_Id] = None,        # Before time path
                            areas    : List[Safe_Id] = None,        # After time path
                            file_id  : Safe_Id       = None,        # File components
                            extension: str           = None
                       ) -> Safe_Str__File__Path:                               # Generate a flexible path with optional time components and organizational elements."""

        path = ""
        if domains:                                                             # Build domains part (if any)
            path += '/'.join(str(domain) for domain in domains)


        time_parts = []                                                         # Build time path with any available components - fully independent
        if year is not None:
            time_parts.append(f'{year:04}')
        if month is not None:
            time_parts.append(f'{month:02}')
        if day is not None:
            time_parts.append(f'{day:02}')
        if hour is not None:
            time_parts.append(f'{hour:02}')

        if time_parts:                                                          # Add timeparts (if any)
            if path:
                path += '/' + '/'.join(time_parts)
            else:
                path = '/'.join(time_parts)

        if areas:                                                               # Add areas (if any)
            if path:
                path += '/' + '/'.join(str(area) for area in areas)
            else:
                path = '/'.join(str(area) for area in areas)

        if file_id and extension:                                               # Add file ID and extension (if any)
            if path:
                path += f'/{file_id}.{extension}'
            else:
                path = f'{file_id}.{extension}'

        return Safe_Str__File__Path(path)

    @type_safe
    def from_date_time(self, date_time  : datetime            ,
                             domains    : List[Safe_Id] = None,
                             areas      : List[Safe_Id] = None,
                             file_id    : Safe_Id       = None,
                             extension  : str           = None
                        ) -> Safe_Str__File__Path:                              # Generate a path from a datetime object.
        return self.generate_path(year      = date_time.year ,
                                  month     = date_time.month,
                                  day       = date_time.day  ,
                                  hour      = date_time.hour ,
                                  domains   = domains        ,
                                  areas     = areas          ,
                                  file_id   = file_id        ,
                                  extension = extension      )

    @type_safe
    def now(self, domains   : List[Safe_Id] = None,
                  areas     : List[Safe_Id] = None,
                  file_id   : Safe_Id       = None,
                  extension : str           = None,
                  now       : datetime      = None
             ) -> Safe_Str__File__Path:                                  # Generate a path using current time or provided timestamp.
        date_time = now or datetime.now()
        return self.from_date_time(date_time = date_time,
                                   domains   = domains  ,
                                   areas     = areas    ,
                                   file_id   = file_id  ,
                                   extension = extension)