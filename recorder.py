# 简单录音机
# 录制麦克风音频并保存为wav文件到当前文件夹

# 引入库
import pyaudio
import wave

# 定义常量
# 格式
FORMAT = pyaudio.paInt16
# 采样率
FS = 44100
# 通道
CHANNELS = 1
# 缓存块大小
CHUNK = 1024
# 录制音频时间（秒）
RECORD_SECOND = 5

# 创建对象
p = pyaudio.PyAudio()
# 输入麦克风音频
stream = p.open(format=FORMAT, channels=CHANNELS, rate=FS,
                input=True, frames_per_buffer=CHUNK)
print('* 开始录音了')

# 缓存数据
frames = []
#采样次数 = 录制时间 * 采样率 / 缓存块
numTimes = int(RECORD_SECOND * FS / CHUNK)
# 读取数据
for i in range(numTimes):
    data = stream.read(CHUNK)
    frames.append(data)
print('完成')

stream.start_stream()
#关闭资源
stream.close()
p.terminate()

#转换保存数据为wav
#获取位深
sampleWidth = p.get_sample_size(FORMAT)
#保存为wav
wf = wave.open("output.wav", 'wb')
#设置通道数
wf.setnchannels(CHANNELS)
#设置位深
wf.setsampwidth(sampleWidth)
#设置采样率
wf.setframerate(FS)
#写文件
wf.writeframes(b''.join(frames))
#关闭资源
wf.close()