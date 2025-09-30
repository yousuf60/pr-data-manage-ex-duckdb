import polars as pl
from .duck import DBDuck, ic


# get polars DataFrame
class DTPolars(DBDuck):
    
    def __init__(self, duck, store_pl=False):
        # copy the essential settings from duck instance
        self.store_command = ic(duck.store_command)
        self.delete_command = ic(duck.delete_command)
        self.table_name = duck.table_name
        self.file_path = ic(duck.file_path)
        self.con = duck.con
        self.save = duck.save
        
    def show(self):
        self._select_all()
        return self.pl()

    # kwargs column:value
    def filter(self,  **kwargs):
        filter_lst = []
        for k, v in kwargs.items():
            if str(v) :
                filter_lst.append(pl.col(k) == v )

        return  self.pl().filter(                    
                      *filter_lst  
                    )

    def update(self,  **kwargs):
        self._update(**kwargs)
        return self.pl()
