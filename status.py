import time, multiprocessing, sys, os
from reprint import output
class prog:
	def __init__(self, forr=False, many=10):
		self.forr = forr
		self.many = many
		self.it = 0
		self.start = 0
		self.adv = []
		self.coun = 0
		self.last = 0
		try:
			self.go()
		except KeyboardInterrupt:
			self.t1.terminate()
			self.t2.terminate()
			print(1)
	def prin(self, what):
		if type(what) == type([]):
			return
		what = what.split("\n")
		with output() as o:
			for i in what:
				o.append(i)
			time.sleep(0.09)
			o.clear()

	def thread(self, pipe):
		p_output, p_input = pipe
		p_input.close()
		while True:
			try:
				adv = p_output.recv()
			except:
				adv = None
			self.prin(adv)
	def thread2(self, con, pipe):
		while True:
			f = self.display(con)
			pipe[1].send(f)
			time.sleep(0.08)
	def log(self, coun=None):
		if self.it == 0:
			self.start = time.time()
			self.last = time.time()
		else:
			self.t2.terminate()
		self.it += 1
		self.adv.append(round(time.time()- self.last, 2))
		self.coun += coun
		self.last= time.time()
		con = [self.it, self.adv,self.coun, self.start, self.last]
		self.t2 = multiprocessing.Process(target=self.thread2, args=(con, self.pipe,))
		self.t2.daemon = True
		self.t2.start()
	def go(self):
		p_output, p_input = multiprocessing.Pipe()
		self.pipe = (p_output,p_input)
		self.t1 = multiprocessing.Process(target=self.thread, args=((p_output, p_input),))
		self.t1.daemon = True
		self.t1.start()
		p_output.close()
	def display(self, adv):
		self.adv = adv[1]
		self.start = adv[3]
		self.it=adv[0]
		self.coun=adv[2]
		self.last = adv[4]
		try:
			st = f"Iterations: {self.it} \nCount: {self.coun} \nElapsed: {round(time.time()-self.start, 3)} \nSince last: {round(time.time()- self.last, 3)} \nAdverage time: {round(sum(self.adv)/(len(self.adv)-1), 2)}"
		except:
			st = [""]
			#self.prin(self.adv)
		return st
