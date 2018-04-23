import struct
import sys

from PIL import Image


# 将二进制文件分解为一个位数组
def decompose(data):
	v = []
	
	# 处理文件为 4 bytes
	fSize = len(data)
	bytes = [ord(chr(b)) for b in struct.pack("i", fSize)]
	
	bytes += [ord(chr(b)) for b in data]

	for b in bytes:
		for i in range(7, -1, -1):
			v.append((b >> i) & 0x1)

	return v

# 将一个位数组组成一个二进制文件
def assemble(v):    
	data_bytes = ""

	length = len(v)
	for idx in range(0, int(len(v)/8)):
		byte = 0
		for i in range(0, 8):
			if (idx*8+i < length):
				byte = (byte<<1) + v[idx*8+i]                
		data_bytes = data_bytes + chr(byte)

	trans = data_bytes.encode()
	payload_size = struct.unpack("i", trans[:4])[0]

	return trans[4: payload_size + 4]

# 设置第 i 位的值为 x
def set_bit(n, i, x):
	mask = 1 << i
	n &= ~mask
	if x:
		n |= mask
	return n

def embed(imgFile, payload):
	# 处理原始图像
	img = Image.open(imgFile)
	(width, height) = img.size
	conv = img.convert("RGBA").getdata()
	print("[*] Input image size: %sx%s pixels." % (width, height))
	max_size = width*height*3.0/8/1024		# 最大存放数据
	print("[*] Usable payload size: %.2f KB." % (max_size))

	f = open(payload, "rb")
	data = f.read()
	f.close()
	print("[+] Payload size: %.3f KB " % (len(data)/1024.0))
		
	data_enc = data

	v = decompose(data_enc)
	
	# 增加到3的倍数
	while(len(v)%3):
		v.append(0)

	payload_size = len(v)/8/1024.0
	print("[+] Encrypted payload size: %.3f KB " % (payload_size))
	if (payload_size > max_size - 4):
		print("[-] Cannot embed. File too large.")
		sys.exit()
		
	# 生成输出图像
	steg_img = Image.new('RGBA',(width, height))
	data_img = steg_img.getdata()

	idx = 0

	for h in range(height):
		for w in range(width):
			(r, g, b, a) = conv.getpixel((w, h))
			if idx < len(v):
				r = set_bit(r, 0, v[idx])
				g = set_bit(g, 0, v[idx+1])
				b = set_bit(b, 0, v[idx+2])
			data_img.putpixel((w,h), (r, g, b, a))
			idx = idx + 3
    
	steg_img.save(imgFile + "-stego.bmp", "BMP")
	
	print("[+] %s embedded successfully!" % payload)

# 提取嵌入到输入文件LSB中的数据
def extract(in_file, out_file):
	img = Image.open(in_file)
	(width, height) = img.size
	conv = img.convert("RGBA").getdata()
	print("[+] Image size: %dx%d pixels." % (width, height))

	v = []
	for h in range(height):
		for w in range(width):
			(r, g, b, a) = conv.getpixel((w, h))
			v.append(r & 1)
			v.append(g & 1)
			v.append(b & 1)
			
	data_out = assemble(v)

	data_dec = data_out

	out_f = open(out_file, "wb")
	out_f.write(data_dec)
	out_f.close()
	
	print("[+] Written extracted data to %s." % out_file)

if __name__ == "__main__":
	if sys.argv[1] == "hide":		
		embed(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "extract":
		extract(sys.argv[2], sys.argv[3])
	else:
		print("[-] Invalid operation specified")