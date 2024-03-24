import backend.task as task
import backend.Task_Matvey as TasMat

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

initial_phase_of_the_received_pulse = 30
initial_frequency = 2
wavelength_of_the_emitted_signal = 4
radial_velocity_of_the_target = 15
intermediate_frequency_of_the_receiver = 2
amplitude = 3

dat = TasMat.GraphDate()
abscissa_2 = 0.0
while abscissa_2 <= 100:
    interface_2 = TasMat.Interfaces()
    interface_2.__int__(initial_phase_of_the_received_pulse, initial_frequency,
                        wavelength_of_the_emitted_signal, radial_velocity_of_the_target,
                        intermediate_frequency_of_the_receiver, amplitude)
    ordinate = interface_2.get_frequency_1(abscissa_2)
    dat.append_x(abscissa_2)
    dat.append_y(ordinate)
    abscissa_2 += 0.5

TasMat.drawchart(dat, 'Quasi-continuous signal')

frequency_deviation = 30
pulse_duration = 20

date = TasMat.GraphDate_2()
while abscissa_2 <= 100:
    interface_2 = TasMat.Interfaces()
    interface_2.__int__(initial_phase_of_the_received_pulse, initial_frequency,
                        wavelength_of_the_emitted_signal, radial_velocity_of_the_target,
                        intermediate_frequency_of_the_receiver, amplitude, frequency_deviation, pulse_duration)
    ordinate = interface_2.get_frequency_2(abscissa_2)
    dat.append_x(abscissa_2)
    dat.append_y(ordinate)
    abscissa_2 += 0.5

TasMat.drawchart(dat, 'Signal_with_linear_frequency_modulation')
