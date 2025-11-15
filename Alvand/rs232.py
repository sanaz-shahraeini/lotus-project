import serial
import serial.tools.list_ports

# نمایش پورت‌های موجود
print([p.device for p in serial.tools.list_ports.comports()])

ser = serial.Serial(
    port="COM3",      # پورت خودتان
    baudrate=9600,    # از دفترچه دستگاه
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1,        # برای جلوگیری از بلاک شدن
)

try:
    while True:
        data = ser.readline()  # تا \n می‌خواند؛ اگر باینری است از read() استفاده کنید
        if data:
            text = data.decode(errors="ignore").strip()
            print(text)
finally:
    ser.close()