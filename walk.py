import sys
import time
import os
from PIL import Image
direction = [ '左', '上', '下', '右' ]
direction_sig = [ '←', '↑', '↓', '→']
last_time = 0
path = []
pos = []
# 检测是否存在度为0或者为'1'的点
# 如果存在度为0的点,又不是终点,则该情况不符合
# 如果存在两个或两个以上的度为1的点,又不可回退,则也不行
def check(grid, w, h, cur):
	list0 = [] # 记录度为1的点
	for x in range(w):
		for y in range(h):
			if grid[y][x] == 1:
				du = 0
				du0 = 0
				for i in range(-1, 2, 1):
					for j in range(-1, 2, 1):
						if i * j != 0 or i + j == 0:
							continue
						if y+j < h and y+j > -1 and x+i < w and x+i > -1:
							if grid[y+j][x+i] == 1:
								du += 1
							elif grid[y+j][x+i] == cur:
								du0 += 1
				if du == 0:
					return False
				elif du == 1 and du0 != 1:
					list0.append([y, x])
					if len(list0) == 2:
						if (list0[0][0]-list0[1][0])*(list0[0][1]-list0[1][1]) != 0:
							return False
					elif len(list0) > 2:
						return False
	return True
# 深度遍历即可
# path 放置每次走的方向
# grid 记录当前地图的映射以及每次走的位置
# grid_map 与手机屏幕坐标对应
# w h 宽多少格,高多少格
# l 总共有多少格
# curx cury 当前的位置
def walk(path, grid, grid_map, w, h, l, curx, cury):
	global direction, pos, direction_sig, last_time
	if len(path) == l:
		print('路径:')
		print(path)
		#print(pos)
		for i in grid:
			for j in i:
				if j == -1:
					print(' * ', end='')
				elif j == 0:
					print('   ', end='')
				else:
					print('%2d ' % j, end='')
			print()
		print('计算用时:', round(time.time() - last_time, 3), 's')
		last_time = time.time()
		
		for i in pos:
			x = i[0]
			y = i[1]
			os.system('adb shell input tap %d %d' % (grid_map[i[0]][i[1]][0], grid_map[i[0]][i[1]][1]))
			time.sleep(0.1)
		'''
		for i in range(len(pos) - 1):
			x0 = pos[i][0]
			y0 = pos[i][1]
			x1 = pos[i+1][0]
			y1 = pos[i+1][1]
			os.system('adb shell input swipe %d %d %d %d 100' % (grid_map[x0][y0][0], grid_map[x0][y0][1], grid_map[x1][y1][0], grid_map[x1][y1][1]))
		'''
		print('操作用时:', round(time.time() - last_time, 3), 's\n')
		last_time = time.time()
		return True
	dir = -1
	for i in range(-1, 2, 1):
		for j in range(-1, 2, 1):
			if i * j != 0 or i + j == 0:
				continue
			dir += 1
			if cury+j < h and cury+j > -1 and curx+i < w and curx+i > -1:
				if grid[cury+j][curx+i] == 1:
					#print('curx = %d cury = %d' % (curx, cury))
					#print('i = %d j = %d' % (i, j))
					
					path.append(direction[dir])
					pos.append([cury+j, curx+i])
					grid[cury+j][curx+i] = len(path)
					if len(path) == l - 1:
						if walk(path, grid, grid_map, w, h, l, curx+i, cury+j):
								return True
					else:
						if check(grid, w, h, len(path)):
							if walk(path, grid, grid_map, w, h, l, curx+i, cury+j):
								return True	
					path.pop()
					pos.pop()
					grid[cury+j][curx+i] = 1
	return False
def get_screen(path):
	redirect2null = '>/dev/null'
	if os.name == 'nt':
		redirect2null = '>nul'
	os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png %s' % redirect2null)
	os.system('adb pull /sdcard/screenshot.png %s %s' % (path, redirect2null))
# 获得图片中每个格子的尺寸
def get_scale(path):
	im = Image.open(path)
	x,y,w,h = 0, 355, 1080, 1350
	im = im.crop((x,y,x+w,y+h))
	pix = im.load()
	y0 = 10
	minx,maxx=1080,0
	miny,maxy=1350+355,0
	for y in range(10, 1350, 2):
		flag = False
		for x in range(150, 1080, 10):
			if pix[x, y] == (209, 209, 209, 255):
				flag = True
				break
		if flag:
			y0 = y
			break
	x0 = 10
	for x in range(10, 1080, 2):
		flag = False
		for y in range(y0, 1350, 10):
			if pix[x, y] == (209, 209, 209, 255):
				x0 = x
				flag = True
				break
		if flag:
			break
	#print('x0 = %d y0 = %d' % (x0, y0))
	# x0 y0 为第一个检测到的位置
	# 向下检测得到尺寸1
	x1 = x0 + 10
	count = 0
	width1 = 0
	for y in range(10, 1350, 2):
		if pix[x1, y] != (249, 249, 249, 255) and count % 2 == 1:
			#print('下', x1, y, '背景', count)
			width1 = y - width1
			count += 1
		if pix[x1, y] == (249, 249, 249, 255) and count % 2 == 0:
			#print('下', x1, y, '方格', count)
			count += 1
		if count == 4:
			break
	# 向右检测得到尺寸2
	y1 = y0 + 10
	count = 0
	width2 = 0
	for x in range(10, 1080, 1):
		if pix[x, y1] != (249, 249, 249, 255) and count % 2 == 1:
			#print('右', x, y1, '背景', count)
			width2 = x - width2
			count += 1
		if pix[x, y1] == (249, 249, 249, 255) and count % 2 == 0:
			#print('右', x, y1, '方格', count)
			count += 1
		
		if count == 4:
			break
	#print('width1 = %d width2 = %d' % (width1, width2))
	# 考虑到格子之间可能不连续,所以取两者的最小值作为尺寸
	return x0, y0, min(width1, width2)
# 将图片抽象成列表返回
def get_map(path):
	im = Image.open(path)
	x,y,w,h = 0, 355, 1080, 1350
	# 裁剪出主要部分
	im = im.crop((x,y,x+w,y+h))
	#im.save('1.png')
	pix = im.load()
	all_list = []
	# 获得左上角第一个格子的位置（不管存不存在）以及格子尺寸
	x0, y0, scale = get_scale(path)
	x0 += int(scale/2)
	y0 += int(scale/2)
	#print('scale =', scale)
	minx,maxx=1080,0
	miny,maxy=1350+355,0
	# 遍历每一行
	#print('x0 = %d y0 = %d' % (x0, y0))
	for y in range(y0, 1350, scale):
		# 遍历每一列的每一行
		list0 = []
		for x in range(x0, 1080, scale):
			#print('( %d, %d )' % (x, y+355))
			#print(pix[x, y])
			if pix[x, y] == (209, 209, 209, 255):
				#print('(%d, %d)' % (x, y))
				if x > maxx:
					maxx = x
				if x < minx:
					minx = x
				if y+355 > maxy:
					maxy = y+355
				if y+355 < miny:
					miny = y+355
				list0.append([x, y+355])
			elif pix[x,y] != (249, 249, 249, 255):
				#print('(%d, %d)' % (x, y))
				#print(pix[x, y])
				list0.append([x, 0])
		if len(list0) != 0:
			all_list.append(list0)
	
	#先获得检测到的y的最小值与最大值,以此来确定每一列的长度
	grid_map = []
	grid = []
	#print('minx = %d maxx = %d' % (minx, maxx))
	for i in all_list:
		list1 = []
		list2 = []
		for x in range(minx, maxx+1, scale):	
				if x in [x0[0] for x0 in i]:
					tmp = [x0 for x0 in i if x0[0] == x][0]
					list1.append(tmp)
					if tmp[1] == 0:
						list2.append(-1)
					else:
						list2.append(1)
				else:
					list1.append([-1, -1])
					list2.append(0)
		grid_map.append(list1)
		grid.append(list2)
	'''
	for i in grid:
		print(i)
	for i in grid_map:
		print(i)
	'''
	return grid, grid_map
	
# 获得输入
def get_count():
	count = 0
	while True:
		try:
			count = int(input('请输入当前的关数(1-615):'))
			if count >= 1 and count <= 615:
				return count
			else:
				print('输入有误,请重新输入')
		except:
			print('输入有误,请重新输入')

def main():
	global path, pos, last_time
	count = 1
	if len(sys.argv) != 2:
		count = get_count()
	else:
		try:
			count = int(sys.argv[1])
			if not count >= 1 and count <= 405:
				count = get_count()
		except:
			count = get_count()
	while True:
		print('当前第 %d 关' % (count))
		path = []
		pos = []
		# 截取主游戏屏幕并自动进行游戏
		
		#此处循环检测是否已经下一关可以开始了,否则则就等待一下
		while True:
			get_screen('./shot.png')
			pix = Image.open('./shot.png').load()
			if pix[530, 910] == (171, 221, 12, 255):
				os.system('adb shell input tap 555 1255')
				time.sleep(1)
			else:
				break
		grid, grid_map = get_map('./shot.png')
		startx, starty = 0, 0
		l = 0
		if len(grid) == 0:
			print(grid)
			print(grid_map)
			print('错误: 获取信息失败1')
			sys.exit(-1)
		# 遍历得到开始格子的位置,以及总共的格子数
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 1:
					l += 1
				elif grid[i][j] == -1:
					startx, starty = j, i
		last_time = time.time()
		# 执行
		path.append([startx, starty])
		walk(path, grid, grid_map, len(grid[0]), len(grid), l+1, startx, starty)
		count += 1
		if count == 406 + 210:
			print('恭喜获得所有的喵,客官慢走哈～')
			sys.exit(0)
		time.sleep(1.5)
		# 点击下一关按钮
		os.system('adb shell input tap 555 1255')
		os.system('adb shell input tap 555 1255')
		time.sleep(3)
		# 判断是下一喵还是下一关
		if count % 15 == 1:
			print('下一喵')
			time.sleep(2)
			get_screen('./shot.png')
			pix = Image.open('./shot.png').load()
			if pix[530, 1300] == (171, 221, 0, 255):
				os.system('adb shell input tap 530 1400')
				time.sleep(2)
				os.system('adb shell input tap 245 410')
				time.sleep(2)
			else:
				print('pix[530, 910] = ', pix[530, 910])
				print('未知错误,退出')
				sys.exit(-1)
		
if __name__ == '__main__':
	main()
