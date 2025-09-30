"""parquet version"""
import os
from icecream import ic
import duckdb  

class DBDuck:
    table_name = "TBL"
    file_path = "data/dt/ex1.db"
    def __init__(self, table_name = None, file_path = None ,
                 columns =  "(a1 VARCHAR, a2 integer, a3 integer )"):
        #custom table name of the DT instance
        if table_name:self.table_name = table_name
        #custom file path of the table of the DT instance
        if file_path:self.file_path = file_path
            
        #using whatever number of columns replace it with "?" 
        #wich is needed for store command
        values_sandwich = "( "+",".join(tuple("?" for _ in columns.split(",") )) + ")"
        self.store_command = f"INSERT INTO {self.table_name}  VALUES" + values_sandwich
        
        self.delete_command = "DELETE FROM " + self.table_name
        
        self.connect_to_file_path()
        self.con.sql(f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} """ + columns
)
        
    def connect_to_file_path(self):
        self.con = duckdb.connect(self.file_path)
        ic("made file connection")
        
    #temporary example for start 
    def _tempex(self, number_of_rows):
        import random 
        import string
        # random strings 
        def rw(n):
            return "".join([random.choice(string.ascii_letters) for _ in range(n)])

        # random number 
        def rn(n):
            return int(random.random()*n)
        
        self.insert_rows([rw(3), rn(5), rn(2)] for _ in range(number_of_rows))
         


    def _select_all(self):
        self.con.execute(f"select * from {self.table_name}")
        
    def show(self)->list[tuple[str,int,int]]:
        self._select_all()
        return self.con.fetchall()

    def pl(self):
        self._select_all()
        return self.con.pl()

    # insert one row [str, int, int]
    def insert_row(self, row: list ):
        self.con.execute(self.store_command,
                        ic(
                            row
                        )
                    )

                    
    # insert list or generator(yield fn) of rows  
    #  [ [str, int, int], ...]
    def insert_rows(self, row: list[list]):
        
    
        self.con.executemany(self.store_command,
            
                [*row] # this way so we may use generator with yield
            
        )    
        

    def _add_where_clause(self, *args, **kwargs):
        return self._add_for_params_clause(*args, **kwargs)       
                 
    def _add_for_params_clause(self, command:str,
                        alter:str|None = " WHERE ", alter_and:str|None = " AND ",
                        **kwargs # your columns and the values given to =? params
                        ):
                        
        command += alter
        params = []
        cols = ic(list(kwargs.items()))
        ln = len(cols)
        for index in range(ln):
            k = cols[index][0]
            v = cols[index][1]
            #to make sure it is not empty string  
            if str(v): 
                command += k + "=? "
                params.append(v)
            # put and if the is more than one column passed
            if index != ln-1:
                command += alter_and + " "
                
        return [ic(command), params]
         
        
    # remove row 
    def delete(self, **kwargs):
        
                    
        self.con.execute(
            *self._add_where_clause(self.delete_command, 
                                        **kwargs)
        )
        
    # clear table
    def clear(self):
        
        self.con.sql(
            self.delete_command
        )
        
    # update row 
    # to=> {"a1":..., "a2": ...}
    def _update(self, to,**kwargs):
        command = "UPDATE " + self.table_name
        command , params1 =  ic(self._add_for_params_clause(command, **to,
                               alter = " SET ", alter_and = " , " ))
        command , params2 = ic(self._add_where_clause(command, **kwargs))
        
        self.con.execute(
            command,
            params1+params2
        )
    
    def update(self,  **kwargs):
        self._update(**kwargs)
        return self.con.fetchall()
        
    def _filter(self, **kwargs):
         
        self.con.execute(
           *self._add_where_clause("SELECT * from  " + self.table_name,
                                       **kwargs)
            
        )
    
    def filter(self,  **kwargs):
        self._filter(**kwargs)
        return self.con.fetchall()

    def remove(self):
        os.remove(self.file_path)
    
    def drop(self):
        self.con.sql(
            "DROP TABLE " + self.table_name 
        )

    
    def save(self, file = None):
        if file:
            self.copy_table_to(file)
    
    def copy_table_to(self, file: str):
        self.con.sql(ic("COPY "+self.table_name+" TO "+f"'{file}'"))


#it is named ParquetDuck but what if use it for other file types
class PQDuck(DBDuck):
    file_path = "data/dt/ex1.parquet"
    
    def __init__(self, *args, **kawrgs):
        super().__init__(*args, **kawrgs)
        
        if not os.path.exists(self.file_path):
            self.con.sql(f"""
        COPY {self.table_name} TO '{self.file_path}' 
            """)
            
        self.con.sql(f"""
        COPY {self.table_name} FROM '{self.file_path}' """
        )

    
    def save(self, file = None):
        if not file:
            file = self.file_path
        self.copy_table_to(file)
            
        

    # necessary to connect to our own parquet not ordinary dt file
    def connect_to_file_path(self):
        self.con = duckdb.connect()
        
