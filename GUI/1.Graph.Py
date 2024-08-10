import spidev
import time
from RPi import GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
from gpiozero import LED,Button
from matplotlib import pyplot as plt
#sw1 = Button(26,pull_up=True)#  37
#from gpiozero import LED,Button
from scipy.ndimage import gaussian_filter1d
from scipy import signal
import gpiod
from time import sleep

button_pin_1 =  26 #13
button_pin_2 =  13
chip = gpiod.Chip("gpiochip4")

cs_line = chip.get_line(19)  # GPIO19
cs_line.request(consumer="SPI_CS", type=gpiod.LINE_REQ_DIR_OUT)
cs_line.set_value(1)  # Set CS high initially

button_line_1 = chip.get_line(button_pin_1)
button_line_1.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN)


button_line_2 = chip.get_line(button_pin_2)
button_line_2.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN)

spi = spidev.SpiDev()

spi.open(0,0)
spi.max_speed_hz  = 4000000#600000
spi.lsbfirst=False
spi.mode=0b01
spi.bits_per_word = 8

spi_2 = spidev.SpiDev()

spi_2.open(0,1)
spi_2.max_speed_hz=4000000#600000
spi_2.lsbfirst=False
spi_2.mode=0b01
spi_2.bits_per_word = 8

who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 print ("data", read_reg)
 
def send_command(command):
 send_data = [command]
 com_reg=spi.xfer(send_data)
 
def write_byte(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)

def read_byte_2(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 cs_line.set_value(0)
 read_reg=spi.xfer(data)
 cs_line.set_value(1)
 print ("data", read_reg)
 
def send_command_2(command):
 send_data = [command]
 cs_line.set_value(0)
 spi_2.xfer(send_data)
 cs_line.set_value(1)
 
def write_byte_2(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)

 cs_line.set_value(0)
 spi_2.xfer(data)
 cs_line.set_value(1)

 

send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

write_byte (0x14, 0x80) #GPIO 80
write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xFF)
write_byte (0x04, 0x00)
write_byte (0x0D, 0x00)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
#
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)

send_command (rdatac)
send_command (start)


send_command_2 (wakeup)
send_command_2 (stop)
send_command_2 (reset)
send_command_2 (sdatac)

write_byte_2 (0x14, 0x80) #GPIO 80
write_byte_2 (config1, 0x96)
write_byte_2 (config2, 0xD4)
write_byte_2 (config3, 0xFF)
write_byte_2 (0x04, 0x00)
write_byte_2 (0x0D, 0x00)
write_byte_2 (0x0E, 0x00)
write_byte_2 (0x0F, 0x00)
write_byte_2 (0x10, 0x00)
write_byte_2 (0x11, 0x00)
write_byte_2 (0x15, 0x20)
#
write_byte_2 (0x17, 0x00)
write_byte_2 (ch1set, 0x00)
write_byte_2 (ch2set, 0x00)
write_byte_2 (ch3set, 0x00)
write_byte_2 (ch4set, 0x00)
write_byte_2 (ch5set, 0x00)
write_byte_2 (ch6set, 0x00)
write_byte_2 (ch7set, 0x00)
write_byte_2 (ch8set, 0x00)

send_command_2 (rdatac)
send_command_2 (start)

DRDY=1

result=[0]*27
result_2=[0]*27


data_1ch_test = []
data_2ch_test = []
data_3ch_test = []
data_4ch_test = []
data_5ch_test = []
data_6ch_test = []
data_7ch_test = []
data_8ch_test = []

data_9ch_test = []
data_10ch_test = []
data_11ch_test = []
data_12ch_test = []
data_13ch_test = []
data_14ch_test = []
data_15ch_test = []
data_16ch_test = []

axis_x=0
y_minus_graph=100
y_plus_graph=100
x_minux_graph=5000
x_plus_graph=250
sample_len = 250

fig, axis = plt.subplots(4, 4, figsize=(5, 5))
plt.subplots_adjust(hspace=1)
ch_name = 0
ch_name_title = [1,5,2,6,3,7,4,8]
axi = [(i, j) for i in range(4) for j in range(2)]
for ax_row, ax_col in axi:
    axis[ax_row, ax_col].set_xlabel('Time')
    axis[ax_row, ax_col].set_ylabel('Amplitude')
    axis[ax_row, ax_col].set_title('Data after pass filter Ch-' + str(ch_name_title[ch_name]))
    ch_name = ch_name + 1    
    
test_DRDY = 5 
test_DRDY_2 = 5
#1.2 Band-pass filter
data_before = []
data_after =  []
just_one_time = 0
data_lenght_for_Filter = 2     # how much we read data for filter, all lenght  [_____] + [_____] + [_____]
read_data_lenght_one_time = 1   # for one time how much read  [_____]
sample_len = 250
sample_lens = 250
fps = 250
highcut = 1
lowcut = 10
data_before_1 = data_before_2 = data_before_3 = data_before_4 = data_before_5 = data_before_6 = data_before_7 = data_before_8 = [0]*250
data_before_9 = data_before_10 = data_before_11 = data_before_12 = data_before_13 = data_before_14 = data_before_15 = data_before_16 = [0]*250

print (data_lenght_for_Filter*read_data_lenght_one_time-read_data_lenght_one_time)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

while 1:
    
    
    #print ("1", button_state)
    #print("2", button_state_2)

        #print ("ok3")
        button_state = button_line_1.get_value()
        #print (button_state)
        if button_state == 1:
            test_DRDY = 10
        if test_DRDY == 10 and button_state == 0:
            test_DRDY = 0 

            output=spi.readbytes(27)
            
            cs_line.set_value(0)
            output_2=spi_2.readbytes(27)
            cs_line.set_value(1)

#            print (output[0],output[1],output[2])
            if output_2[0]==192 and output_2[1] == 0 and output_2[2] == 8:
                #print ("ok4")
                for a in range (3,25,3):
                    voltage_1=(output[a]<<8)| output[a+1]
                    voltage_1=(voltage_1<<8)| output[a+2]
                    convert_voktage=voltage_1|data_test
                    if convert_voktage==data_check:
                        voltage_1_after_convert=(voltage_1-16777214)
                    else:
                       voltage_1_after_convert=voltage_1
                    channel_num =  (a/3)

                    result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

                data_1ch_test.append(result[1])
                data_2ch_test.append(result[2])
                data_3ch_test.append(result[3])
                data_4ch_test.append(result[4])
                data_5ch_test.append(result[5])
                data_6ch_test.append(result[6])
                data_7ch_test.append(result[7])
                data_8ch_test.append(result[8])


                for a in range (3,25,3):
                    voltage_1=(output_2[a]<<8)| output_2[a+1]
                    voltage_1=(voltage_1<<8)| output_2[a+2]
                    convert_voktage=voltage_1|data_test
                    if convert_voktage==data_check:
                        voltage_1_after_convert=(voltage_1-16777214)
                    else:
                       voltage_1_after_convert=voltage_1
                    channel_num =  (a/3)

                    result_2[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

                data_9ch_test.append(result_2[1])
                data_10ch_test.append(result_2[2])
                data_11ch_test.append(result_2[3])
                data_12ch_test.append(result_2[4])
                data_13ch_test.append(result_2[5])
                data_14ch_test.append(result_2[6])
                data_15ch_test.append(result_2[7])
                data_16ch_test.append(result_2[8])


                
                
                if len(data_9ch_test)==sample_len:


                    data_after_1 = data_1ch_test        
                    dataset_1 =  data_before_1 + data_after_1
                    data_before_1 = dataset_1[250:]
                    data_for_graph_1 = dataset_1

                    data_filt_numpy_high_1 = butter_highpass_filter(data_for_graph_1, highcut, fps)
                    data_for_graph_1 = butter_lowpass_filter(data_filt_numpy_high_1, lowcut, fps)

                    axis[0,0].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_1[250:], color = '#0a0b0c')  
                    axis[0,0].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_1[50]-y_minus_graph, data_for_graph_1[150]+y_plus_graph])

                    # 2
                    data_after_2 = data_2ch_test        
                    dataset_2 =  data_before_2 + data_after_2
                    data_before_2 = dataset_2[250:]
                    data_for_graph_2 = dataset_2

                    data_filt_numpy_high_2 = butter_highpass_filter(data_for_graph_2, highcut, fps)
                    data_for_graph_2 = butter_lowpass_filter(data_filt_numpy_high_2, lowcut, fps)

                    axis[1,0].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_2[250:], color = '#0a0b0c')  
                    axis[1,0].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_2[50]-y_minus_graph, data_for_graph_2[150]+y_plus_graph])

                    # 3
                    data_after_3 = data_3ch_test        
                    dataset_3 =  data_before_3 + data_after_3
                    data_before_3 = dataset_3[250:]
                    data_for_graph_3 = dataset_3

                    data_filt_numpy_high_3 = butter_highpass_filter(data_for_graph_3, highcut, fps)
                    data_for_graph_3 = butter_lowpass_filter(data_filt_numpy_high_3, lowcut, fps)

                    axis[2,0].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_3[250:], color = '#0a0b0c')  
                    axis[2,0].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_3[50]-y_minus_graph, data_for_graph_3[150]+y_plus_graph])

                    # 4
                    data_after_4 = data_4ch_test        
                    dataset_4 =  data_before_4 + data_after_4
                    data_before_4 = dataset_4[250:]
                    data_for_graph_4 = dataset_4

                    data_filt_numpy_high_4 = butter_highpass_filter(data_for_graph_4, highcut, fps)
                    data_for_graph_4 = butter_lowpass_filter(data_filt_numpy_high_4, lowcut, fps)

                    axis[3,0].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_4[250:], color = '#0a0b0c')  
                    axis[3,0].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_4[50]-y_minus_graph, data_for_graph_4[150]+y_plus_graph])

                    #5
                    data_after_5 = data_5ch_test        
                    dataset_5 =  data_before_5 + data_after_5
                    data_before_5 = dataset_5[250:]
                    data_for_graph_5 = dataset_5

                    data_filt_numpy_high_5 = butter_highpass_filter(data_for_graph_5, highcut, fps)
                    data_for_graph_5 = butter_lowpass_filter(data_filt_numpy_high_5, lowcut, fps)

                    axis[0,1].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_5[250:], color = '#0a0b0c')  
                    axis[0,1].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_5[50]-y_minus_graph, data_for_graph_5[150]+y_plus_graph])
                     
                    #6
                    data_after_6 = data_6ch_test        
                    dataset_6 =  data_before_6 + data_after_6
                    data_before_6 = dataset_6[250:]
                    data_for_graph_6 = dataset_6

                    data_filt_numpy_high_6 = butter_highpass_filter(data_for_graph_6, highcut, fps)
                    data_for_graph_6 = butter_lowpass_filter(data_filt_numpy_high_6, lowcut, fps)

                    axis[1,1].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_6[250:], color = '#0a0b0c')  
                    axis[1,1].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_6[50]-y_minus_graph, data_for_graph_6[150]+y_plus_graph])

                    #7
                    data_after_7 = data_7ch_test        
                    dataset_7 =  data_before_7 + data_after_7
                    data_before_7 = dataset_7[250:]
                    data_for_graph_7 = dataset_7

                    data_filt_numpy_high_7 = butter_highpass_filter(data_for_graph_7, highcut, fps)
                    data_for_graph_7 = butter_lowpass_filter(data_filt_numpy_high_7, lowcut, fps)

                    axis[2,1].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_7[250:], color = '#0a0b0c')  
                    axis[2,1].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_7[50]-y_minus_graph, data_for_graph_1[150]+y_plus_graph])

                    #8
                    data_after_8 = data_8ch_test        
                    dataset_8 =  data_before_8 + data_after_8
                    data_before_8 = dataset_8[250:]
                    data_for_graph_8 = dataset_8

                    data_filt_numpy_high_8 = butter_highpass_filter(data_for_graph_8, highcut, fps)
                    data_for_graph_8 = butter_lowpass_filter(data_filt_numpy_high_8, lowcut, fps)

                    axis[3,1].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_8[250:], color = '#0a0b0c')  
                    axis[3,1].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_8[50]-y_minus_graph, data_for_graph_8[150]+y_plus_graph])
                    
                    # 9
                    data_after_9 = data_9ch_test        
                    dataset_9 =  data_before_9 + data_after_9
                    data_before_9 = dataset_9[250:]
                    data_for_graph_9 = dataset_9

                    data_filt_numpy_high_9 = butter_highpass_filter(data_for_graph_9, highcut, fps)
                    data_for_graph_9 = butter_lowpass_filter(data_filt_numpy_high_9, lowcut, fps)

                    axis[0,2].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_9[250:], color = '#0a0b0c')  
                    axis[0,2].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_9[50]-y_minus_graph, data_for_graph_9[150]+y_plus_graph])

                    # 10
                    data_after_10 = data_10ch_test        
                    dataset_10 =  data_before_10 + data_after_10
                    data_before_10 = dataset_10[250:]
                    data_for_graph_10 = dataset_10

                    data_filt_numpy_high_10 = butter_highpass_filter(data_for_graph_10, highcut, fps)
                    data_for_graph_10 = butter_lowpass_filter(data_filt_numpy_high_10, lowcut, fps)

                    axis[1,2].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_10[250:], color = '#0a0b0c')  
                    axis[1,2].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_10[50]-y_minus_graph, data_for_graph_10[150]+y_plus_graph])

                    # 11
                    data_after_11 = data_11ch_test        
                    dataset_11 =  data_before_11 + data_after_11
                    data_before_11 = dataset_11[250:]
                    data_for_graph_11 = dataset_11

                    data_filt_numpy_high_11 = butter_highpass_filter(data_for_graph_11, highcut, fps)
                    data_for_graph_11 = butter_lowpass_filter(data_filt_numpy_high_11, lowcut, fps)

                    axis[2,2].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_11[250:], color = '#0a0b0c')  
                    axis[2,2].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_11[50]-y_minus_graph, data_for_graph_11[150]+y_plus_graph])

                    # 12
                    data_after_12 = data_12ch_test        
                    dataset_12 =  data_before_12 + data_after_12
                    data_before_12 = dataset_12[250:]
                    data_for_graph_12 = dataset_12

                    data_filt_numpy_high_12 = butter_highpass_filter(data_for_graph_12, highcut, fps)
                    data_for_graph_12 = butter_lowpass_filter(data_filt_numpy_high_12, lowcut, fps)

                    axis[3,2].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_12[250:], color = '#0a0b0c')  
                    axis[3,2].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_12[50]-y_minus_graph, data_for_graph_12[150]+y_plus_graph])

                    # 13
                    data_after_13 = data_13ch_test        
                    dataset_13 =  data_before_13 + data_after_13
                    data_before_13 = dataset_13[250:]
                    data_for_graph_13 = dataset_13

                    data_filt_numpy_high_13 = butter_highpass_filter(data_for_graph_13, highcut, fps)
                    data_for_graph_13 = butter_lowpass_filter(data_filt_numpy_high_13, lowcut, fps)

                    axis[0,3].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_13[250:], color = '#0a0b0c')  
                    axis[0,3].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_13[50]-y_minus_graph, data_for_graph_13[150]+y_plus_graph])
                     
                    # 14 
                    data_after_14 = data_14ch_test        
                    dataset_14 =  data_before_14 + data_after_14
                    data_before_14 = dataset_14[250:]
                    data_for_graph_14 = dataset_14

                    data_filt_numpy_high_14 = butter_highpass_filter(data_for_graph_14, highcut, fps)
                    data_for_graph_14 = butter_lowpass_filter(data_filt_numpy_high_14, lowcut, fps)

                    axis[1,3].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_14[250:], color = '#0a0b0c')  
                    axis[1,3].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_14[50]-y_minus_graph, data_for_graph_14[150]+y_plus_graph])

                    # 15
                    data_after_15 = data_15ch_test        
                    dataset_15 =  data_before_15 + data_after_15
                    data_before_15 = dataset_15[250:]
                    data_for_graph_15 = dataset_15

                    data_filt_numpy_high_15 = butter_highpass_filter(data_for_graph_15, highcut, fps)
                    data_for_graph_15 = butter_lowpass_filter(data_filt_numpy_high_15, lowcut, fps)

                    axis[2,3].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_15[250:], color = '#0a0b0c')  
                    axis[2,3].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_15[50]-y_minus_graph, data_for_graph_15[150]+y_plus_graph])

                    # 16
                    data_after_16 = data_16ch_test        
                    dataset_16 =  data_before_16 + data_after_16
                    data_before_16 = dataset_16[250:]
                    data_for_graph_16 = dataset_16

                    data_filt_numpy_high_16 = butter_highpass_filter(data_for_graph_16, highcut, fps)
                    data_for_graph_16 = butter_lowpass_filter(data_filt_numpy_high_16, lowcut, fps)

                    axis[3,3].plot(range(axis_x,axis_x+sample_lens,1),data_for_graph_16[250:], color = '#0a0b0c')  
                    axis[3,3].axis([axis_x-x_minux_graph, axis_x+x_plus_graph, data_for_graph_16[50]-y_minus_graph, data_for_graph_16[150]+y_plus_graph])


                    plt.pause(0.0000000000001)
                    
                    axis_x=axis_x+sample_lens 
                    data_1ch_test = []
                    data_2ch_test = []
                    data_3ch_test = []
                    data_4ch_test = []
                    data_5ch_test = []
                    data_6ch_test = []
                    data_7ch_test = []
                    data_8ch_test = []
                    data_9ch_test = []
                    data_10ch_test = []
                    data_11ch_test = []
                    data_12ch_test = []
                    data_13ch_test = []
                    data_14ch_test = []
                    data_15ch_test = []
                    data_16ch_test = []
                

spi.close()






