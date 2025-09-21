- DBDuck
	- /__init__  << (tablename file_path custom_duckdb_columns="(x int, ...)")
	- show()     << select all and return them  fetchall()
	- filter     << kwargs=col1=...,...
	- delete     << kwargs=col1=...,...    kwargs of where clause
	- drop       == drops the table
	- insert_row << [val1, val2, ...]
	- insert_rows<< [row1, row2, row3]    and can be generator (yield row1,...)
	- clear()    ==  clears column items
	- update     << kwargs of columns , to={"col1":val, ...}  put kwargs for the where clause and to for SET
	- remove()   == remove file in file_path

- PQDuck
	child of DBDuck to support parquet file
	- save() == copy to file_path   otherwise the data will not be saved
