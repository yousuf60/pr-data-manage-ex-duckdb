from data import DTDuck, DTPolars, ic
ic.enabled = True

dt = DTDuck("EX")
dt._tempex(10)
#dt.show()
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

dt2 = DTPolars(dt)


ic(
dt2.show(),
dt2.filter(a2=0)
)

dt.clear()

ic(
dt2.show(),
dt2.filter(a2=0)
)

dt.drop()
del dt, dt2


dt = DTDuck("EX", columns = "(name varchar, id integer)")
dt.insert_row(["kcpckpw", 198])
dt.insert_row(["kcpckpw", 198])
ic(dt.show())
dt.drop()
