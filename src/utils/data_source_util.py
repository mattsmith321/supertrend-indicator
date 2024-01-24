

class DataSourceUtil:
    def __init__(self, name, api_key, source_column_name):
        self.name = name
        self.class_name = name.replace(' ', '')
        self.api_key = api_key
        self.source_column_name = source_column_name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__()