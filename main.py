from data import DTDuck, DTPolars, ic
ic.enabled = True

dt = DTDuck("EX")
dt._tempex(30)
#dt.show()
dt.filter(a2=0)
# dt.insert_row(["beeeeb", 238, 28956])

#dt.delete(a2=0,a3=0)
# dt.filter(a2=0, a3=0)
dt.show()
#dt.update(a2=0, to=(None, None, 0))
dt.filter(a2=0)


dt2 = DTPolars(dt)


ic(
dt2.show()
)

dt.clear()

ic(
dt2.show(),
dt2.filter(a2=0)
)
