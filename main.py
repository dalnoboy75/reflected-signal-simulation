import backend.task as task

adopted_power_ = 2.0
emitter_power_ = 2.0
amplification_coefficient_ = 3.0
wavelength_ = 4.0
reflective_area_ = 5.0
damage_coefficient_ = 1.0

data = task.GraphData()
abscissa_ = 0.0
abscissa_label = 'adopted_power_'
while abscissa_ <= 100:
    interface = task.Interface()
    interface.__int__(abscissa_, emitter_power_, amplification_coefficient_, wavelength_, reflective_area_,
                      damage_coefficient_)
    ordinate = interface.get_distance()
    if ordinate != None:
        data.append_x(abscissa_)
        data.append_y(ordinate)

    abscissa_ += 0.001

task.draw_chart(data, "charts", abscissa_label)
