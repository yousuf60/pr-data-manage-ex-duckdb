from data import DT
dt = DT()
dt._tempex()
dt.show()
# dt.filter(a2=0, a3=0)
# dt.delete(a2=0,a3=0)
# dt.filter(a2=0, a3=0)
# dt.clear()
dt.show()
dt.update(a2=1, to=(None, 3, 0))
dt.filter(a2=3)

