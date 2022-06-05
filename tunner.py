# 吉他调音器

# 导入库
import pyaudio
import numpy as np
from scipy import signal
import matplotlib as mpl
import matplotlib.pyplot as plt

# 转换度为弧度
def d2r(degree): return degree * np.pi / 180.

# 定义终止函数【意义同示波器】
def on_press(event):
    global in_stream, p, END
    if event.key == 'q':
        END = True
        plt.close()
        in_stream.stop_stream()
        in_stream.close()
        p.terminate()


# =============================================================================
# Notes_guitar =['E2','A2','D3','G3','B3','E4']
# 六根弦对应音符和频率
notesGuitar = ['E', 'A', 'D', 'G', 'B', 'E']
freqGuitar = np.array(
    [82.4096, 110.0000, 146.8324, 195.9977, 246.9417, 329.6276])
# 表盘上显示的关键刻度
freqTicks = np.array([0, 82.4096, 90, 110.0000, 146.8324,
                     180, 195.9977, 246.9417, 270, 329.6276])
tickNotes = ['0Hz', 'E', '90', 'A', 'D', '180', 'G', 'B', '270', 'E']
# =============================================================================

FORMAT = pyaudio.paInt16
CHANNELS = 1
SAMPLE_RATE = 3000
SAMPLE_INTERVAL = 1/SAMPLE_RATE
END = False
# 一段音频持续的时间
T = 2
# 调音器的分辨率(Hz)，傅里叶变换后两个相邻频率点之间的频率间隔
RES = 1./T
# 一小段音频的采样点的数目
CHUNK = T*SAMPLE_RATE

# 初始化麦克风输入
p = pyaudio.PyAudio()
in_stream = p.open(format=FORMAT, channels=CHANNELS,
                   rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)

# 作图参数设置
# 面板半径
r_panel = 30
# 指针长度
pointer_len = r_panel - 1
# 指针颜色
pointer_color = '#E7E0CD'
# 指针宽度
pointer_width = 1
# 频谱图最低位置
spectrum_base = 15
# 频谱赋值缩小的倍数，目的是让图像尽量不超出面板
divide_factor = 20
# 不显示工具栏
mpl.rcParams['toolbar'] = 'None'
fig = plt.figure()
# 字体加粗
plt.rcParams["font.weight"] = "bold"
# 主面板背景色
fig.patch.set_facecolor('#F7FBF8')
# fig.canvas.toolbar_visible = False
# 使用极坐标
ax = plt.subplot(projection='polar')
# 调音器面板颜色设置
ax.set_facecolor('#305996')
# 窗口名字
plt.get_current_fig_manager().set_window_title(
    'GuitarTuner  Bylsl312 【按Q可以退出~ Press Q to exit~】')
# 绑定按键退出函数
fig.canvas.mpl_connect('key_press_event', on_press)
# 画表盘上的主要刻度
ax.set_xticks(d2r(freqTicks))
ax.set(xticklabels=tickNotes)
# 调音面板半径的范围
ax.set_ylim(0, 30)
# ax.set_yticks([30])
# 取消显示调音面板半径的值
ax.set(yticklabels=[])
# 调音面板外边框的颜色
ax.spines['polar'].set_color('#305996')
# 频谱线的颜色
ax.tick_params(axis='x', color='#305996')
plt.grid()

# 表盘上的小刻度
scale = np.arange(0, 360, 10)
# 控制刻度其实位置的参数
scale_end_r = r_panel
scale_start_r = r_panel - 1
# 控制刻度宽度的参数
scale_w_min = 0.7
scale_w_max = 2.0

# 指针的起点：在中心画一个小圆圈
ax.scatter(0, 0, c=pointer_color, s=32, cmap='hsv', alpha=1)
# 画主次要的刻度
for s in scale:
    ax.vlines(d2r(s), scale_end_r, scale_start_r,
              colors=pointer_color, linewidth=scale_w_min, zorder=3)
# 画主要刻度
for f in freqGuitar:
    ax.vlines(d2r(f), scale_end_r, scale_start_r,
              colors=pointer_color, linewidth=scale_w_max, zorder=3)

# 带通滤波器保留的频率范围
lowcut, highcut = 75.0, 1250.0
# 吉他空弦的频率范围
freq_range = [75, 350]
# 傅里叶变换后的横坐标
freq = np.fft.rfftfreq(CHUNK, d=SAMPLE_INTERVAL)
# 通过它得到吉他空弦的频率范围外的范围
mask = (freq < freq_range[0]) + (freq > freq_range[1])

# 待画的频率范围
mask_plot = freq < 360
# 选择要画的那段频率
freq_to_plot = freq[mask_plot]
# 画弧度谱
line0, = ax.plot(d2r(freq_to_plot), 50*np.random.rand(len(freq_to_plot)),
                 color=pointer_color, linewidth=pointer_width)

# 开启交互模式
plt.ion()
plt.tight_layout()
plt.show()

# 主体
while END == False:
    # 读取十六进制的数据到缓冲区;
    buffer = in_stream.read(CHUNK, exception_on_overflow=False)
    # 转化缓冲区的数据为16位的整型数据
    y = np.frombuffer(buffer, dtype=np.int16)
    # 对时域信号做傅立叶变换, 因为是输入是实数，我们使用rfft, 没有用fft。
    Y = np.fft.rfft(y)/CHUNK
    # 得到幅度谱
    Y_a = np.abs(Y)
    # 带通滤波器
    sos = signal.butter(10, [lowcut, highcut], 'bp',
                        fs=SAMPLE_RATE, output='sos')
    filtered = signal.sosfilt(sos, y)
    FILTERED = np.fft.rfft(filtered)/CHUNK
    FILTERED_a = np.abs(FILTERED)
    S_a = FILTERED_a
    # 强行让吉他音频范围以外的频率幅值归零
    S_a[mask] = 0
    # 找到幅值最大的频率
    main_freq = freq[np.argmax(S_a)]
    # 画幅度谱
    line0.set_ydata(spectrum_base+FILTERED_a[mask_plot]/divide_factor)
    # 将指针指到最大的频率位置
    vline = ax.vlines(d2r(main_freq), 0, pointer_len, colors=pointer_color,
                      linewidth=pointer_width, zorder=3)
    # 更新画布
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.0001)
    vline.remove()  # 擦出指针旧的位置
