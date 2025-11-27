from f_psl.datetime import UDateTime


for format in UDateTime.Format:
    dt = UDateTime.str_now(format)
    print(format.name, dt)
