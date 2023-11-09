import pandas as pd

class MeasurementDataTables:

    def __init__(self):
        self._hidden_friendly_name: dict = {}
        self._hidden_table_plt_functions: dict = {}

    def append(self, new_table: pd.DataFrame, name, friendly_name=None):
        if friendly_name is None:
            friendly_name = name
        self.__setattr__(name, new_table)
        self._hidden_friendly_name[name] = friendly_name

        return getattr(self, name)

    def add_plot(self, name, plot_function = None):
        if plot_function:
            self._hidden_table_plt_functions[f"{name}"] = plot_function
        return getattr(self, name)

    def update(self, new_table: pd.DataFrame, name):
        self.__setattr__(name, new_table)
        return getattr(self, name)

    def to_list(self) -> list[(pd.DataFrame, str, str)]:
        # write a function that returns all attributes of this class
        return [
            (getattr(self, a), str(a), str(self._hidden_friendly_name[a])) for a in dir(self)
            if not a.startswith('__')
               and not callable(getattr(self, a))
               and not '_hidden' in str(a)
        ]

    def get(self, table_name: str) -> pd.DataFrame:
        return getattr(self, table_name)

    def get_plot_function(self, name):
        return self._hidden_table_plt_functions[name]

    def get_plot_function_names(self):
        return self._hidden_table_plt_functions.keys()

    def plot(self):
        pass
