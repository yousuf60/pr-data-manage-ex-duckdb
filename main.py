from data import PQDuck, DBDuck, DTPolars, ic
ic.enabled = True

dt = DBDuck()
# dt = PQDuck()
dt._tempex(20)

#dt.show()
@lambda _:_()
def sqling():
    dt.show()
    dt.insert_row(["beeeeb", 0, 28956])
    ic(dt.filter(a2=0),
    dt.filter(a2=0, a3=0),
    dt.delete(a2=0,a3=0),
    dt.filter(a2=0, a3=0),
    #dt.show()
    dt.update(a2=0, to={"a2":100}),
    dt.filter(a2=0),
    dt.filter(a2=100)

    )
    
    dt.save()
    
@lambda _:_()
def polars():
    global dt
    dt2 = ic(DTPolars(dt))
    ic(
    dt2.show(),
    dt2.filter(a2=0),
    dt2.filter(a2=100)
    )

    dt.clear()

    ic(
    dt2.show(),
    dt2.filter(a2=100)
    )

    # dt.drop()
    dt2.save()
    del dt


# dt = DBDuck("EX", columns = "(name varchar, id integer)")
dt = PQDuck(file_path="data/dt/fl.parquet", columns = "(name varchar, id integer)")
@lambda _:_()
def extra():
    dt.insert_row(["kcpckpw", 198])
    dt.insert_row(["kcpckpw", 198])
    dt.insert_rows([
        ["kcfwfd", 1928],
        ["kwwbrw", 19458],
        ["kcpowipw", 1948],
        ["kcpwckpwvnvw", 191248],
    ])
    ic(dt.show())
    dt.clear()
    # dt.drop()
    dt.save()
