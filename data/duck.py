from icecream import ic
import duckdb  

class DTDuck:
    table_name = "AZ"
    file_path = "data/dt/ex1.db"    
    def __init__(self, table_name = None, file_path = None ):
        #custom table name of the DT instance
        if table_name:self.table_name = table_name
        #custom file path of the table of the DT instance
        if file_path:self.file_path = file_path
        
        self.store_command = f"INSERT INTO {self.table_name} VALUES(?, ?, ?)"
        self.delete_command = "DELETE FROM " + self.table_name
        
        self.con = duckdb.connect(self.file_path)
        self.con.sql(f"""
CREATE TABLE IF NOT EXISTS {self.table_name} (a1 VARCHAR, a2 integer, a3 integer )
        """
        )

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
            ic(
                [*row] # this way so we may use generator with yield
            )
        )    
        

    def _add_where_clause(self, *args, **kwargs):
        return self._add_for_params_clause(*args, **kwargs)       
                 
    def _add_for_params_clause(self, command:str,
                        a1:str=None, a2:int=None, a3:int=None, 
                        alter:str|None = " WHERE ", alter_and:str|None = " AND "
                        ):
                        
        command += alter
        params = []
        
        if a1 is not None:
            command += "a1=? "
            params.append(a1)
            
        if a2 is not None:
            command += (alter_and if a1 is not None else "")+ "a2=? " + (alter_and if a3 is not None else "")
            params.append(a2)
            
        if a3 is not None:
            command += "a3=? "
            params.append(a3)
        return [command, params]
         
        
    # remove row 
    def delete(self, **kwargs):
        
                    
        self.con.execute(
            *ic(self._add_where_clause(self.delete_command, 
                                        **kwargs) )
        )
        
    # clear table
    def clear(self):
        
        self.con.sql(
            self.delete_command
        )
        
    # update row 
    # to=> (a1|None, a2|None, a3|None)
    def _update(self, to,**kwargs):
        command = "UPDATE " + self.table_name
        command , params1 =  ic(self._add_for_params_clause(command, a1=to[0], a2=to[1], a3=to[2],
                               alter = " SET ", alter_and = " , " ))
        command , params2 = ic(self._add_where_clause(command, **kwargs))
        
        self.con.execute(
            command,
            params1+params2
        )
    
    def update(self,  **kwargs):
        self._update(**kwargs)
        return self.con.fetchall()
        
    def _filter(self, a1:str=None, a2:int=None, a3:int=None):
         
        self.con.execute(
           *ic(self._add_where_clause("SELECT * from  " + self.table_name,
                                       a1=a1,a2=a2,a3=a3)
            )
        )
    
    def filter(self,  **kwargs):
        self._filter(**kwargs)
        return self.con.fetchall()
