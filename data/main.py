from icecream import ic
ic.enabled = True

import duckdb  
class DT:

    store_command = "INSERT INTO AZ VALUES(?, ?, ?)"
    delete_command = "DELETE FROM AZ "
    file_path = "data/dt/ex1.db"    
    def __init__(self):
        self.con = duckdb.connect(self.file_path)
        self.con.sql("""
CREATE TABLE IF NOT EXISTS AZ(a1 VARCHAR, a2 integer, a3 integer )
        """)

    #temporary example for start 
    def _tempex(self):
        import random 
        import string
        # random strings 
        def rw(n):
            return "".join([random.choice(string.ascii_letters) for _ in range(n)])

        def rn(n):
            return int(random.random()*n)
        
        self.insert_rows([rw(3), rn(5), rn(2)] for _ in range(10))
         


    def show(self)->list[tuple[str,int,int]]:
        self.con.execute("select * from AZ")
        return ic(self.con.fetchall())


    # insert one row [str, int, int]
    def insert_row(self, rows: list ):
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
        

    def add_where_clause(self, *args, **kwargs):
        return self.add_for_params_clause(*args, **kwargs)       
                 
    def add_for_params_clause(self, command:str,
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
            *ic(self.add_where_clause(self.delete_command, 
                                        **kwargs) )
        )
        
    # clear table
    def clear(self):
        
        self.con.sql(
            self.delete_command
        )
        
    # update row 
    # to=> (a1|None, a2|None, a3|None)
    def update(self, to,**kwargs):
        command = "UPDATE AZ"
        command , params1 =  ic(self.add_for_params_clause(command, a1=to[0], a2=to[1], a3=to[2],
                               alter = " SET ", alter_and = " , " ))
        command , params2 = ic(self.add_where_clause(command, **kwargs))
        
        self.con.execute(
            command,
            params1+params2
        )
        return ic(self.con.fetchall()    )
    def filter(self, a1:str=None, a2:int=None, a3:int=None):
         
        self.con.execute(
           *ic(self.add_where_clause("SELECT * from az ",
                                       a1=a1,a2=a2,a3=a3)
            )
        )
        return ic(self.con.fetchall())
