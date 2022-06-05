# 简单示波器

# 引入库
import pyaudio
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#定义终止函数
def on_press(event):
    global stream, p, END
    if event.key == 'q':
        plt.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        END = True

# 常量
#停止标签
END = False
# 一次操作多少数据
CHUNK = 1024
# 格式
FORMAT = pyaudio.paInt16
# 通道数目
CHANNEL = 1
# 采样率
RATE = 44100

# 实例化
p = pyaudio.PyAudio()
# 创建一个流
stream = p.open(format=FORMAT, channels=CHANNEL, rate=RATE,input=True, frames_per_buffer=CHUNK)

#去除工具栏
mpl.rcParams['toolbar'] = 'None'
#创建图像
fig, ax = plt.subplots(figsize=(12,3))
#添加按下事件
fig.canvas.mpl_connect('key_press_event',on_press)
#调整图像大小
plt.subplots_adjust(left=0.001, top=0.999, right=0.999, bottom=0.001)
#修改窗口标题
plt.get_current_fig_manager().set_window_title(
    'ShowWave  Bylsl312 【按Q可以退出~ Press Q to exit~】')
#转化数组
x = np.arange(0,CHUNK)
#画线
line, = ax.plot(x, np.random.rand(CHUNK),color = '#C04851')
#设置x,y轴范围
ax.set_xlim(0,CHUNK-1)
ax.set_ylim(-2**12,2**12)
#关闭坐标轴显示
plt.axis('off')

#开启交互模式
plt.ion()
plt.show()

#获取数据
while END == False:
    data = stream.read(CHUNK,exception_on_overflow=False)
    data = np.frombuffer(data, dtype=np.int16)
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.01)