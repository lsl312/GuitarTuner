#频谱仪

#导入库
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy.fft import rfft, rfftfreq

#输入音频参数设置【意义同示波器】
END = False
audioFmt = pyaudio.paInt16
channelNum = 1
sampleRate = 2200
sampleInterval = 1/sampleRate
sampleTime = 0.1
chunk = int(sampleTime/sampleInterval)
p = pyaudio.PyAudio()
stream = p.open(format=audioFmt,channels=channelNum,rate=sampleRate,input=True,frames_per_buffer=chunk)

#定义终止函数【意义同示波器】
def on_press(event):
    global stream, p, END
    if event.key == 'q':
        plt.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        END = True


#作图设置【意义同示波器】
mpl.rcParams['toolbar'] = 'None'
fig, ax = plt.subplots(figsize=(12,3))
fig.canvas.mpl_connect('key_press_event',on_press)
plt.subplots_adjust(left=0.001, top=0.999, right=0.999, bottom=0.001)
plt.get_current_fig_manager().set_window_title(
    'Spectrum  Bylsl312 【按Q可以退出~ Press Q to exit~】')

#得到傅里叶变换的横坐标
freq = rfftfreq(chunk, d=sampleInterval)
#获取y数据
y_data = np.random.rand(freq.size)
#画线
line, = ax.step(freq,y_data,where='mid',color='#C04851')
#人声频率范围
ax.set_xlim(80,1100)
#y轴范围
ax.set_ylim(-1000,1000)
#关闭坐标轴
plt.axis('off')
#开启交互模式
plt.ion()
plt.show()

while END == False:
    #获取数据
    data = stream.read(chunk,exception_on_overflow=False)
    #转换为16位整型
    data = np.frombuffer(data, dtype=np.int16)
    #对实数序列做傅里叶变换
    X = rfft(data)
    #得到幅度，适当缩放
    y_data = np.abs(X)*0.01
    #更新y坐标数据
    line.set_ydata(y_data)
    #填充颜色
    axfill = ax.fill_between(freq, 0, y_data, step="mid",color='#C04851',alpha=0.7)
    axfill_ = ax.fill_between(freq, 0, -1*y_data, step="mid",color='#C04851',alpha=0.075)
    #画图像
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)
    #删除填充区域
    axfill.remove()
    axfill_.remove()
