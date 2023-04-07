import tkinter as tk
from tkinter import font as f, scrolledtext as stxt, messagebox as msg, filedialog
import subprocess, os, json, sys, time, keyword, re, chardet, signal, platform
from threading import *
from multiprocessing import *
class txtedit(tk.Frame):
	def __init__(self, fps_limit, master = None):
		Thread(target=self.autosaver, daemon=True, name="AutoSaver").start()
		self.fps = fps_limit
		super().__init__(master)
		self.pack(fill = tk.BOTH, expand = True)
		f1 = f.Font(size = 12)
		global txt, nowdata, editmenu, runmenu, nowfile, sbar, sbartxt
		nowdata = ""
		nowfile = ""
		root.title(lang[setjs["gui"]["lang"]][1] + " - " + lang[setjs["gui"]["lang"]][0])
		root.geometry("1140x520")
		root.minsize(760, 420)

		menubar = tk.Menu(self)
		filemenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		editmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		runmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		viewmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		setmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		helpmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		langmenu = tk.Menu(viewmenu, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		runpyset = tk.Menu(setmenu, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		convmenu = tk.Menu(menubar, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		encmenu = tk.Menu(convmenu, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		reopmenu = tk.Menu(convmenu, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")
		encset = tk.Menu(setmenu, tearoff = 0, background="#ffffff", activebackground = "#e3e3e3", foreground = "#333333", activeforeground = "#000000")

		convmenu.add_cascade(label = lang[setjs["gui"]["lang"]][26], menu=encmenu)
		convmenu.add_cascade(label = lang[setjs["gui"]["lang"]][27], menu=reopmenu)
		
		encmenu.add_command(label="Shift-JIS", command=lambda: self.enc("cp932"))
		encmenu.add_command(label="JIS", command=lambda: self.enc("iso-2022-jp"))
		encmenu.add_command(label="(UTF-16-LE)", command=lambda: self.enc("utf-16-le"))
		encmenu.add_command(label="(UTF-16-BE)", command=lambda: self.enc("utf-16-be"))
		encmenu.add_command(label="UTF-8", command=lambda: self.enc("utf-8"))
		encmenu.add_command(label="UTF-7", command=lambda: self.enc("utf-7"))
		encmenu.add_separator()
		encmenu.add_command(label="US-ASCII", command=lambda: self.enc("ascii"))

		reopmenu.add_command(label="Shift-JIS", command=lambda: self.reop("cp932"))
		reopmenu.add_command(label="JIS", command=lambda: self.reop("iso-2022-jp"))
		reopmenu.add_command(label="(UTF-16-LE)", command=lambda: self.reop("utf-16-le"))
		reopmenu.add_command(label="(UTF-16-BE)", command=lambda: self.reop("utf-16-be"))
		reopmenu.add_command(label="UTF-8", command=lambda: self.reop("utf-8"))
		reopmenu.add_command(label="UTF-7", command=lambda: self.reop("utf-7"))
		reopmenu.add_separator()
		reopmenu.add_command(label="US-ASCII", command=lambda: self.reop("ascii"))

		encset.add_command(label="Shift-JIS", command=lambda: self.encset("cp932"))
		encset.add_command(label="JIS", command=lambda: self.encset("iso-2022-jp"))
		encset.add_command(label="UTF-8", command=lambda: self.encset("utf-8"))
		encset.add_command(label="UTF-7", command=lambda: self.encset("utf-7"))

		self.langvar = tk.IntVar(value = setjs["gui"]["lang"])
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][3], command = self.newfile, accelerator = "Ctrl+N")
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][4], command = self.newwindow, accelerator = "Ctrl+Shift+N")
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][5], command = lambda: self.openfile(False, "text", False), accelerator = "Ctrl+O")
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][6], command = self.savefile, accelerator = "Ctrl+S")
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][7], command = lambda: self.saveas(encode), accelerator = "Ctrl+Shift+S")
		filemenu.add_separator()
		self.autosave = tk.IntVar(value = setjs["AutoSave"])
		filemenu.add_checkbutton(label=lang[setjs["gui"]["lang"]][28], command=self.autosaveset, variable=self.autosave)
		filemenu.add_separator()
		filemenu.add_command(label = lang[setjs["gui"]["lang"]][8], command = self.closesavecheck, accelerator = "Alt+F4")

		editmenu.add_command(label = lang[setjs["gui"]["lang"]][10], command = lambda: txtedit.reundo("un"), accelerator = "Ctrl+Z")
		editmenu.add_command(label = lang[setjs["gui"]["lang"]][11], command = lambda: txtedit.reundo("re"), accelerator = "Ctrl+Y")

		runmenu.add_command(label = "Python", command = lambda: self.runpy(True), accelerator = "F5")
		runmenu.add_command(label = lang[setjs["gui"]["lang"]][13], command = lambda: self.runpy(False), accelerator = "Ctrl+F5")
		runmenu.add_command(label = lang[setjs["gui"]["lang"]][14], command = self.cmd, accelerator = "Ctrl+Shift+@")

		runpyset.add_command(label = "Python.exe", command = lambda: self.runpyset("py"))
		runpyset.add_command(label = "Pythonw.exe", command = lambda: self.runpyset("pyw"))

		langmenu.add_radiobutton(label = "English", command = self.radio, variable = self.langvar, value = 0)
		langmenu.add_radiobutton(label = "日本語", command = self.radio, variable = self.langvar, value = 1)

		helpmenu.add_command(label=lang[setjs["gui"]["lang"]][30], command=self.versioninf)

		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][2], menu = filemenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][9], menu = editmenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][25], menu=convmenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][12], menu = runmenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][15], menu = viewmenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][16], menu = setmenu)
		menubar.add_cascade(label = lang[setjs["gui"]["lang"]][29], menu = helpmenu)

		self.fullvar = tk.IntVar(value = 0)
		viewmenu.add_checkbutton(label = lang[setjs["gui"]["lang"]][17], command = lambda: self.fullsc(False), accelerator = "F11", variable = self.fullvar)
		self.wrapvar = tk.IntVar(value = setjs["gui"]["wrap"])
		viewmenu.add_checkbutton(label = lang[setjs["gui"]["lang"]][19], command = self.wrapset, variable = self.wrapvar)
		self.syntvar = tk.IntVar(value=setjs["gui"]["syntax"])
		viewmenu.add_checkbutton(label = lang[setjs["gui"]["lang"]][20], command = self.syntax, variable = self.syntvar)
		self.fpsdvar = tk.IntVar(value = setjs["gui"]["fps"]["display"])
		viewmenu.add_checkbutton(label = lang[setjs["gui"]["lang"]][21], command = self.fpsdispset, variable = self.fpsdvar)

		setmenu.add_cascade(label = lang[setjs["gui"]["lang"]][18], menu = langmenu)
		setmenu.add_cascade(label = "Python", menu = runpyset)
		setmenu.add_cascade(label = lang[setjs["gui"]["lang"]][25], menu = encset)
		setmenu.add_separator()
		setmenu.add_command(label = lang[setjs["gui"]["lang"]][22], command = reset)

		filemenu.bind_all("<Control-n>", self.newfile)
		filemenu.bind_all("<Control-N>", self.newwindow)
		filemenu.bind_all("<Control-s>", self.savefile)
		filemenu.bind_all("<Control-S>", lambda: self.saveas(encode))
		runmenu.bind_all("<F5>", lambda c: self.runpy(True))
		runmenu.bind_all("<Control-F5>", lambda c: self.runpy(False))
		viewmenu.bind_all("<F11>", lambda bind: self.fullsc(True))
		runmenu.bind_all("<Control-`>", self.cmd)

		filemenu["font"] = f1
		editmenu["font"] = f1
		runmenu["font"] = f1
		setmenu["font"] = f1
		viewmenu["font"] = f1
		langmenu["font"] = f1
		runpyset["font"] = f1
		convmenu["font"] = f1
		encmenu["font"] = f1
		reopmenu["font"] = f1
		encset["font"] = f1

		txt = SyntaxHighlightText(self)
		txt["font"] = f1
		txt.pack(fill = tk.BOTH, expand = tk.YES)
		if setjs["gui"]["wrap"] == 1:
			if setjs["gui"]["wrap2"] == "word":
				txt["wrap"] = tk.WORD
			elif setjs["gui"]["wrap2"] == "char":
				txt["wrap"] = tk.CHAR

		txt.bind_all("<<Modified>>", self.titlechange)
		txt.bind_all("<Control-o>", lambda event=None: app.openfile(False, "text", True, event))
		txt.bind("<Button-3>", self.rightclick)

		sbartxt = tk.StringVar()
		sbartxt.set(setjs["gui"]["encode"])
		sbar = tk.Label(self, textvariable = sbartxt, background = "#68217a", foreground = "#ffffff", anchor = "e")
		sbar["font"] = f1
		sbar.pack(fill = tk.BOTH, expand = tk.YES, side = tk.RIGHT)
		self.last_time = time.time()
		self.frame_count = 0
		self.fps_limit = fps_limit
		self.encodeloading = ""
		self.enccheck = False
		self.update_fps()
		root.config(menu = menubar)
		root.iconbitmap(default=f"{setf}\\Content\\notepad.ico")
		root.protocol("WM_DELETE_WINDOW", (lambda: self.closesavecheck)())
	
	def versioninf(self):
		msg.showinfo(title=lang[setjs["gui"]["lang"]][30], message=f"PyNotepad Ver.Beta.{str(version)[0]}.{str(version)[1]}.{str(version)[2]}-{str(version)[3:]}\nCopyright(c) Yamat.72k")

	def autosaver(self):
		while True:
			if setjs["AutoSave"] == 1 and nowfile != "":
				if not(self.filecheck()):
					self.savefile()
			for i in range(60):
				time.sleep(1)
				if win == "false":break

	def autosaveset(self):
		setjs["AutoSave"] = self.autosave.get()
		jsonsave()

	def encset(self, enc):
		global encode
		setjs["gui"]["encode"] = enc
		if nowfile == "":
			encode = enc
		jsonsave()

	def reop(self, to):
		try:
			global nowfile, nowdata, encode, rootopenfile
			if nowfile != "":
				with open(nowfile, "r", encoding=to) as f:
					nowdata = f.read()
				txt.delete("1.0", "end")
				txt.insert("1.0", nowdata)
				encode = to
				Thread(target=txt.highlight, name="highlight").start()
			elif txt.get("1.0", "end-1c") != "":
				encode = to
			else:
				rootopenfile = tk.Toplevel()
				rootopenfile.attributes("-topmost", True)
				rootopenfile.withdraw()
				self.openf(False, "text")
				if nowfile != "":
					self.reop(to)
		except:
			pass

	def enc(self, to):
		global nowdata, nowfile, encode
		path = self.saveas(to, False)
		if path != False:
			if msg.askyesno(title=langmsg[setjs["gui"]["lang"]][14], message=langmsg[setjs["gui"]["lang"]][15]):
				with open(path, "r", encoding=to) as f:
					nowdata = f.read()
				if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
				nowfile = path
				encode = to
				txt.delete("1.0", "end")
				txt.insert("1.0", nowdata)
				Thread(target=txt.highlight, daemon=True, name="highlight")

	def reundo(reun):
		if reun == "re":txt.edit_redo()
		elif reun == "un":txt.edit_undo()

	def syntax(self):
		syntax = self.syntvar.get()
		setjs["gui"]["syntax"] = syntax
		jsonsave()
		txt.on_key_release()

	def update_fps(self):
		self.frame_count += 1
		li = txt.index("insert").split(".")
		temptxt = sbartxt.get()
		if "Pythonw" in temptxt:
			temptxt = f" | Pythonw | {encode}"
		elif "Python" in temptxt:
			temptxt = f" | Python | {encode}"
		else:
			temptxt = f" | {encode}"
		current_time = time.time()
		if current_time - self.last_time >= 1:
			fps = self.frame_count / (current_time - self.last_time)
			fps = round(fps, 2)
			ping = (1/fps)*1000
			ping = round(ping, 2)
			self.fps = f"fps: {fps} | ping: {ping}ms | "
			self.last_time = current_time
			self.frame_count = 0
		if self.fps == self.fps_limit:self.fps = ""
		
		sbartemp = lang[setjs["gui"]["lang"]][23] + str(li[0]) + lang[setjs["gui"]["lang"]][24] + f" {int(li[1]) + 1}{temptxt}"
		if setjs["gui"]["fps"]["display"] == 1:sbartxt.set(self.encodeloading + str(self.fps) + sbartemp)
		elif setjs["gui"]["fps"]["display"] == 0:sbartxt.set(self.encodeloading + sbartemp)
		time_to_wait = max(1, int(1000/self.fps_limit - (time.time() - current_time)*1000))
		root.after(time_to_wait, self.update_fps)

	def radio(self, event = None):
		jsonload()
		if setjs["gui"]["lang"] != self.langvar.get():
			setjs["gui"]["lang"] = self.langvar.get()
			jsonsave()
			fc = self.filecheck()
			if fc == None or fc == True:
				self.closesavecheck()
				if os.path.splitext(selfname)[1] == ".exe":
					txtedit.newwinexeprocess(selfname)
				elif os.path.splitext(selfname)[1] == ".py" or os.path.splitext(selfname)[1] == ".pyw":
					txtedit.newwinprocess(selfname)
			elif fc == False:
				msg.showwarning(title=langmsg[setjs["gui"]["lang"]][12], message=langmsg[setjs["gui"]["lang"]][13])

	def runpyset(self, exe, event = None):
		if exe == "py":
			self.openfile(False, "pyexe", False)
		elif exe == "pyw":
			self.openfile(False, "pywexe", False)

	def titlechange(self, e):
		fc = self.filecheck()
		if fc == False:
			if nowfile != "":
				root.title("*" + nowfile + " - " + lang[setjs["gui"]["lang"]][0])
			else:
				root.title("*" + lang[setjs["gui"]["lang"]][1] + " - " + lang[setjs["gui"]["lang"]][0])
		else:
			if nowfile != "":
				root.title(nowfile + " - " + lang[setjs["gui"]["lang"]][0])
			else:
				root.title(lang[setjs["gui"]["lang"]][1] + " - " + lang[setjs["gui"]["lang"]][0])
		e.widget.edit_modified(False)

	def newwinexeprocess(filepath):subprocess.Popen(filepath, start_new_session=True)
	def newwinprocess(filepath):subprocess.call(["pyw", filepath], start_new_session=True)

	def newwindow(self, event=None):
		if os.path.splitext(selfname)[1] == ".exe":
			Process(target = txtedit.newwinexeprocess, args=(selfname,)).start()
		elif os.path.splitext(selfname)[1] == ".py" or os.path.splitext(selfname)[1] == ".pyw":
			Process(target = txtedit.newwinprocess, args=(selfname,)).start()

	def savecheck(self):
		global nowfile, nowdata
		msgres = msg.askyesnocancel(title = langmsg[setjs["gui"]["lang"]][0], message = langmsg[setjs["gui"]["lang"]][1])
		if msgres:
			if self.savefile():
				return True
		elif msgres == False:
			return False
		return None

	def filecheck(self):
		global nowdata, nowfile
		nowdata = str(txt.get("1.0","end-1c"))
		if nowfile != "":
			with open(nowfile, "r", encoding = encode) as f:
				read = f.read()
			if nowdata == read:
				return True
			else:
				return False
		else:
			if nowdata == "":
				return None
			else:
				return False

	def newfile(self, event = None):
		global nowfile, nowdata
		fc = self.filecheck()
		if fc == None or fc == True:
			nowdata = ""
			if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
			nowfile = ""
			txt.delete("1.0", "end")
		elif nowdata != "\n":
			sc = self.savecheck()
			if sc == True or sc == False:
				txt.delete("1.0", "end")
				if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
				nowfile = ""
				nowdata = ""
		root.title(lang[setjs["gui"]["lang"]][1] + " - " + lang[setjs["gui"]["lang"]][0])

	def encload(self):
		range = 0
		while self.enccheck:
			if range%4 == 0:self.encodeloading = "decoding | "
			if range%4 == 1:self.encodeloading = "decoding. | "
			if range%4 == 2:self.encodeloading = "decoding.. | "
			if range%4 == 3:self.encodeloading = "decoding... | "
			time.sleep(0.6)
			range += 1
		self.encodeloading = ""

	def decoder(self):
		global encode, filename, decodequeue
		decodequeue = Queue()
		decodequeue.put(filename)
		p = Process(target=decoderprocess, args=(decodequeue,), daemon=True)
		p.start()
		time.sleep(5)
		p.terminate()

	def openf(self, c1 , run1):
		def opef():
			global nowdata, nowfile, encode, filename, decodequeue
			if filename != "":
				if os.path.getsize(filename) > 524288:
					sizetemp = os.path.getsize(filename)
					size = str(round(sizetemp/1024, 3)) + " KB (" + str(sizetemp) + "Byte)"
					openyn = msg.askyesno(title = langmsg[setjs["gui"]["lang"]][2], message = langmsg[setjs["gui"]["lang"]][3] + size)
				else:
					openyn = True
				if openyn:
					self.enccheck = True
					lock = open(f"{filename}.lock", "w", encoding="utf-8")
					threadcheck = False
					try:
						with open(filename, "r", encoding="utf-8") as f:
							openfiledata = f.read()
						encode = "utf-8"
					except:
						try:
							with open(filename, "r", encoding="cp932") as f:
								openfiledata = f.read()
							encode = "cp932"
						except:
							encode = setjs["gui"]["encode"]
							th = Thread(target=self.encload, daemon=True, name="loading")
							th.start()
							threadcheck = True
							decode = Thread(target=self.decoder, daemon=True, name="decoder")
							decode.start()
							decode.join()
					self.enccheck = False
					if threadcheck:encode = decodequeue.get()
					if encode == None:
						lock.close()
						if filename != "" and os.path.isfile(f"{filename}.lock"):os.remove(f"{filename}.lock")
						encode = setjs["gui"]["encode"]
						msg.showerror(title = langmsg[setjs["gui"]["lang"]][10], message = langmsg[setjs["gui"]["lang"]][11])
					else:
						try:
							if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
							with open(filename, "r", encoding = encode) as f:
								openfiledata = f.read()
							txt.delete("1.0", "end")
							txt.insert("1.0", openfiledata)
							nowdata = openfiledata
							nowfile = filename
						except Exception as e:
							encode = setjs["gui"]["encode"]
							msg.showerror(title = langmsg[setjs["gui"]["lang"]][10], message = langmsg[setjs["gui"]["lang"]][11] + "\nErrorMessage>>>" + str(e))
			Thread(target=txt.highlight, daemon=True, name="highlight").start()
		global filename
		dirdialog = f"C:\\Users\\{user}\\Downloads"
		if run1 == "pyexe" or run1 == "pywexe":
			dirdialog = f"C:\\Users\\{user}\\AppData\\Local\\Programs\\Python"
		global nowfile, nowdata
		if run1 == "Py":
			typ = [("Python", "*.py *.pyw"), ("TextFile", "*.txt"), ("All Files", "*.*")]
		elif run1 == "text":
			typ = [("All Files", "*.*"), ("TextFile", "*.txt"), ("Python", "*.py *.pyw")]
		elif run1 == "pyexe":
			typ = [("AppFile", "python.exe")]
		elif run1 == "pywexe":
			typ = [("AppFile", "pythonw.exe")]
		filename = filedialog.askopenfilename(title = lang[setjs["gui"]["lang"]][5], filetypes = typ, initialdir = dirdialog)
		rootopenfile.destroy()
		if run1 == "Py":
			opef()
			if nowfile != "":
				Thread(target = lambda : self.runpy(c1), name = "runpy").start()
				return nowfile
			else:return
		elif run1 == "text":
			opef()
			if nowfile != "":
				return nowfile
			else:return
		elif run1 == "pyexe" or run1 == "pywexe":
			jsonload()
			if filename != "":
				if run1 == "pyexe":
					setjs["runpy"]["python.exe"] = filename
				else:
					setjs["runpy"]["pythonw.exe"] = filename
			else:
				setres = msg.askyesno(title = langmsg[setjs["gui"]["lang"]][4], message = langmsg[setjs["gui"]["lang"]][5])
				try:
					if setres:
						if run1 == "pyexe":
							setjs["runpy"]["python.exe"] = "py"
						else:
							setjs["runpy"]["pythonw.exe"] = "pyw"
				except:
					setup()
					jsonload()
			jsonsave()
			return "exe"
		
	def openfile(self, c, run_, focus, event=None):
		if str(txt.focus_get()) != "." and focus == True:
			txt.delete("insert-1c")

		global nowdata, nowfile, rootopenfile
		fc = self.filecheck()
		if run_ == "pyexe" or run_ == "pywexe":
			rootopenfile = tk.Toplevel()
			rootopenfile.attributes("-topmost", True)
			rootopenfile.withdraw()
			Thread(target = lambda: self.openf(c, run_), name = "runexedialog").start()
		elif fc == None or fc == True:
			rootopenfile = tk.Toplevel()
			rootopenfile.attributes("-topmost", True)
			rootopenfile.withdraw()
			Thread(target = lambda: self.openf(c, run_), name = "openfiledialog").start()
		else:
			sc = self.savecheck()
			if sc == False or sc == True:
				rootopenfile = tk.Toplevel()
				rootopenfile.attributes("-topmost", True)
				rootopenfile.withdraw()
				Thread(target = lambda: self.openf(c, run_), name = "openfiledialog").start()

	def savefile(self, event = None):
		nowdata = str(txt.get("1.0","end-1c"))
		if nowfile != "":
			with open(nowfile, "w", encoding = encode) as f:
				f.write(nowdata)
			root.title(nowfile + " - " + lang[setjs["gui"]["lang"]][0])
		else:
			self.saveas(encode, True)

	def saveas(self, enc, yn, event=None):
		global nowfile
		nowdata = str(txt.get("1.0","end-1c"))
		rootsaveas = tk.Toplevel()
		rootsaveas.attributes("-topmost", True)
		rootsaveas.withdraw()
		typ = [("TextFile", "*.txt"), ("Python", "*.py *.pyw"), ("All Files", "*.*"), ("No Extension", "*.")]
		savefilepath = filedialog.asksaveasfilename(title = lang[setjs["gui"]["lang"]][7], defaultextension = ".txt", filetypes = typ)
		rootsaveas.destroy()
		if savefilepath != "":
			if nowfile != "" and yn == True:
				with open(savefilepath, "w", encoding = encode) as f:
					f.write(nowdata.encode(enc).decode(encode))
			else:
				with open(savefilepath, "w", encoding = enc) as f:
					f.write(nowdata.encode(enc).decode(enc))
			if yn:
				if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
				nowfile = savefilepath
				root.title(nowfile)
			else:
				return savefilepath
			return True
		else:
			return False
	
	def runpy(self, c, event = None):
		def thread(c):
			global run, runcheck, procid
			if c:
				sbartxt.set(f"Python | encode")
			else:
				sbartxt.set(f"Pythonw | encode")
			sbar["bg"] = "#cc6633"
			runcheck = True
			if c:
				run = subprocess.Popen([setjs["runpy"]["python.exe"], nowfile], cwd = nowdir)
			else:
				run = subprocess.Popen([setjs["runpy"]["pythonw.exe"], nowfile], cwd = nowdir)
			procid = run.pid
			run.wait()
			runcheck = False
			if win == "y":
				sbartxt.set(encode)
				sbar["bg"] = "#68217a"
				runmenu.entryconfig(0, state = "normal")
				runmenu.entryconfig(1, state = "normal")
		
		global nowdir
		if txt.get("1.0", "end") == "\n":
			self.openfile(c, "Py", False)
		elif nowfile != "":
			self.savefile()
			runmenu.entryconfig(0, state = "disable")
			runmenu.entryconfig(1, state = "disable")
			nowdir = os.path.dirname(nowfile)
			Thread(target = lambda: thread(c), name = "RunPython").start()
		else:
			self.saveas(encode, True)
			if nowfile != "":
				self.runpy(c)

	def cmd(self, event=None):
		def cmdth():
			global run, cmdpid
			run = subprocess.Popen("cmd")
			cmdpid = run.pid
		
		Thread(target = cmdth, name = "cmd").start()

	def closesavecheck(self):
		global win
		fc = self.filecheck()
		if fc == None or fc == True:
			win = "false"
			root.destroy()
		elif fc == False:
			sc = self.savecheck()
			if sc == False or sc == True:
				win = "false"
				root.destroy()

	def killrun():
		if runcheck == True:
			if procid != 0:
				run.send_signal(signal.CTRL_C_EVENT)
		if cmdpid != None:
			subprocess.call("taskkill /F /PID {pid} /T".format(pid = cmdpid), startupinfo = si)
	
	def fpsdispset(self, event = None):
		jsonload()
		setjs["gui"]["fps"]["display"] = self.fpsdvar.get()
		jsonsave()

	def fullsc(self, bind, event = None):
		fullsc = self.fullvar.get()
		if not(bind):
			if fullsc == 0:
				root.attributes('-fullscreen', False)
			elif fullsc == 1:
				root.attributes('-fullscreen', True)
		elif bind:
			if fullsc == 0:
				self.fullvar.set(1)
				root.attributes('-fullscreen', True)
			elif fullsc == 1:
				self.fullvar.set(0)
				root.attributes('-fullscreen', False)
	
	def rightclick(self, e):
		try:editmenu.post(e.x_root, e.y_root)
		except:pass
	
	def wrapset(self):
		jsonload()
		if self.wrapvar.get() == 0:
			txt.configure(wrap=tk.NONE)
			setjs["gui"]["wrap"] = 0
		elif self.wrapvar.get() == 1:
			if setjs["gui"]["wrap2"] == "word":
				txt.configure(wrap=tk.WORD)
			elif setjs["gui"]["wrap2"] == "char":
				txt.configure(wrap=tk.CHAR)
			setjs["gui"]["wrap"] = 1
		jsonsave()

class SyntaxHighlightText(stxt.ScrolledText):
	#Syntax highlighting text widget.
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.configure(wrap=tk.NONE, undo=True)

		self.tag_configure('comment', foreground='green')
		self.tag_configure('number', foreground='green')
		self.tag_configure('kakko', foreground='blue')
		self.tag_configure('function', foreground='blue')
		self.tag_configure('keyword', foreground='blue')
		self.tag_configure('string', foreground='red')
		
		self.highlight_patterns = [
			(re.compile(r'\b%s\b' % w, re.IGNORECASE), 'keyword')
			for w in keyword.kwlist
		]
		self.highlight_patterns.append((re.compile(r"(?<!\\)(?:\\\\)*(['\"])(?:\\.|(?!(?<!\\)\1).)*\1"), "string"))
		self.highlight_patterns.append((re.compile(r'(?<!\S)#.*$', re.MULTILINE), 'comment'))
		self.highlight_patterns.append((re.compile(r'self'), 'function'))
		self.highlight_patterns.append((re.compile(r'\(|\)|\[|\]|\{|\}'), 'kakko'))
		self.highlight_patterns.append((re.compile(r'-?\d+(?:\.\d+)?'), 'number'))
		
		self.bind_class('Text', '<KeyRelease>', self.on_key_release)
		self._highlight_job = None

	def highlight(self):
		nowpath = os.path.splitext(nowfile)[1]
		if setjs["gui"]["syntax"] == 0:return
		if not(nowpath == ".py" or nowpath == ".pyw"):return
		if os.path.getsize(nowfile) > 131072:return
		#Highlight syntax.
		text = self.get('1.0', 'end')

		self.tag_remove('keyword', '1.0', 'end')
		self.tag_remove('string', '1.0', 'end')
		self.tag_remove('comment', '1.0', 'end')
		self.tag_remove('function', '1.0', 'end')
		self.tag_remove('number', '1.0', 'end')
		self.tag_remove('kakko', '1.0', 'end')
		
		for pattern, tag in self.highlight_patterns:
			for match in pattern.finditer(text):
				start, end = match.span()
				start = '1.0+%dc' % start
				end = '1.0+%dc' % end
				self.tag_add(tag, start, end)

	def on_key_release(self, event=None):
		print(self._highlight_job)
		if self._highlight_job:
			self.after_cancel(self._highlight_job)
			try:
				nowpath = os.path.splitext(nowfile)[1]
				if nowpath == ".py" or nowpath == ".pyw":
					if setjs["gui"]["syntax"] == 1:
						self._highlight_job = self.after(1000, self.highlight)
			except:
				pass
		else:
			self._highlight_job = self.after(200, self.highlight)

def decoderprocess(queuep):
	filetemp = queuep.get()
	queuep.put("")
	with open(filetemp, 'rb') as f:
		temp = chardet.detect(f.read())["encoding"]
	queuep.put(temp)

def update():
	print("loading update data")
	time.sleep(0.4)
	print("setup")
	setup()
	print("complete!")
	jsonload()

def setup():
	with open(f"{setf}\\settings.json", "w", encoding = "utf-8") as settxt:
		settxt.write('{"version": ' + str(version) + ', "AutoSave":0, "gui": {"fps": {"limit": 160, "display": 0}, "lang": 0, "wrap": 0, "wrap2": "word", "syntax": 1, "encode": "utf-8"}, "runpy": {"python.exe": "py", "pythonw.exe": "pyw"}, "logging": 0}')

def jsonload():
	try:
		with open(f"{setf}\\settings.json", "r", encoding = "utf-8") as settxt:
			setjs = json.load(settxt)
	except:
		msg.showerror(title = langmsg[setjs["gui"]["lang"]][6], message = langmsg[setjs["gui"]["lang"]][7])

def jsonsave():
	with open(f"{setf}\\settings.json", "w", encoding="utf-8") as f:
		f.write(str(setjs).replace("'", '"'))

def reset():
	setup()
	txtedit.closesavecheck(self=app)
	txtedit.newwindow(self=app)

def clean_up():
	if nowfile != "" and os.path.isfile(f"{nowfile}.lock"):os.remove(f"{nowfile}.lock")
	print("Cleanup was successfully completed.")
def sig_handler():
	sys.exit(1)

if __name__ == "__main__" and platform.system() == "Windows":
	signal.signal(signal.SIGTERM, sig_handler)
	lang = [["Notepad", "Untitled", "File", "New Text File", "New Window", "Open File...", "Save", "Save As...", "Exit", "Edit", "Undo", "Redo", "Run", "Python(noconsole)", "Terminal", "View", "Settings", "Full Screen", "Language", "Word Wrap", "Syntax HighLight", "Show fps", "Reset", "Ln ", ", Col", "Encode", "Convert", "Reopen", "Auto Save", "Help", "About"], 
		["メモ帳", "タイトルなし", "ファイル", "新しいテキストファイル", "新しいウィンドウ", "ファイルを開く...", "保存", "名前を付けて保存...", "終了", "編集", "元に戻す", "やり直し", "実行", "Python(コンソール無し)", "ターミナル", "表示", "設定", "全画面表示", "表示言語", "右端での折り返し", "シンタックスハイライト", "fpsの表示", "リセット", "行 ", "、列", "エンコード", "変換", "再度開く", "自動保存", "ヘルプ", "バージョン情報"]]
	langmsg = [[
			"Save your changes", "Do you want to save the changes you made to file?", 
			"Open File", "Do you want to open a large file?\n", 
			"Settings", "Do you want to reset your settings?", 
			"Json load Error", "settings.json file may have been rewritten.", 
			"Unknown error.", "Unknown error", 
			"Open File Error", "The file is not displayed in the text editor because it is either binary or uses an unsupported text encoding.", 
			"Warning", "A restart is required to apply all settings.", 
			"OpenCheck", "Do you want to open the saved file?"], [
			"変更を保存する", "ファイルに加えた変更を保存しますか？", 
			"ファイルを開く", "サイズの大きいファイルを開きますか?\n", 
			"設定", "設定をリセットしますか?", 
			"Json読み込みエラー", "settings.jsonが書き換えられた可能性があります。", 
			"不明なエラー", "不明なエラーが発生しました。", 
			"Open File エラー", "このファイルはバイナリか、サポートされていないテキスト エンコードを使用しているため、テキストエディタに表示されません。", 
			"注意", "全ての設定を適用するには、再起動が必要です。", 
			"確認", "保存したファイルを開きますか？"]]
	version = 27402
	selfname = sys.argv[0]
	win = "y"
	user = os.getlogin()
	logcheck = 0
	setf = f"C:\\Users\\{user}\\AppData\\Local\\.pynotepad"
	if not(os.path.isdir(setf)):os.makedirs(setf)
	if not(os.path.isdir(f"{setf}\\Content")):os.makedirs(f"{setf}\\Content")
	jsfc = os.path.isfile(f"{setf}\\settings.json")
	if not(os.path.isdir(f"{setf}\\logs")):os.makedirs(f"{setf}\\logs")
	if not(os.path.isfile(f"{setf}\\Content\\notepad.ico")):
		icohexdata = "0000010001002020000001002000a810000016000000280000002000000040000000010020000000000000100000c30e0000c30e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000100000001000000010000000100000001000000010000000100000001000000010000000100000001000000010000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000070000000d0000000f0000000f0000000f0000000f0000000f0000000f0000000f0000000f0000000f0000000f0000000f0000000f000000100000000f0000000d00000007000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000a041d3a3c062a55710629537706295377062953770629537706295377062953770629537706295377062953770629537706295377062953770629537706295377062a5671041d3a3c0000000900000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000101010218074186ad074c9dfd074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074b9bfb074c9efd084287af0102041800000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200020a202a578ec34874a8ff4a74a6ff4973a5ff4973a5ff4973a5ff4973a5ff4973a4ff4973a4ff4872a4ff4872a4ff4872a4ff4872a4ff4872a4ff4872a4ff4872a4ff4673a8ff285992c500040f1f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000206090c20b0b6bdc3dbdde0ffd9daddffd8d9dcffd7d8dbffd7d8dbffd6d8daffd6d7daffd5d7d9ffd5d6d9ffd4d6d9ffd4d5d8ffd3d5d8ffd3d4d7ffd3d4d7ffd3d4d7ffd5d7daffaab1bbc5080c111f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212131620bdb7a5c3d4caa8ffcfc5a2ffcec4a1ffcdc3a0ffcdc29fffccc29effccc19effcbc19dffcbc09cffcabf9cffc9bf9bffc9be9affc8be99ffc8bd99ffc8bd98ffccc29effb8b29ec516171a1f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000210100d20bea655c3dcbe58ffdabc56ffd9bb55ffd8ba53ffd7b952ffd7b851ffd6b74fffd5b64effd4b54dffd3b44bffd2b34affd1b249ffd1b147ffd0b146ffcfb045ffcfb044ffb49b45c514130f1f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002110f0720c1a74ec3dec059ffdcbe57ffdbbd56ffdabc55ffdabb54ffd9ba52ffd8b951ffd7b850ffd6b74effd5b64dffd5b54cffd4b44affd3b449ffd2b348ffd1b246ffd1b145ffb5993bc51411061f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002110f0720c2a850c3dfc15cffddc05affdcbe57ffdabc55ffd9bb54ffd8ba53ffd8b951ffd7b850ffd6b74fffd5b64effd4b54cffd3b44bffd3b34affd2b349ffd2b349ffd2b348ffb69b3dc51411071f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002110f0720c3aa52c3e1c35effddbf5affb6962dffa6841bffa7851bffa6851bffa6841bffa6841affa6841affa68419ffa58319ffa58319ffa48218ffb19026ffd2b349ffd4b54affb89c3fc51411071f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002110f0820c4ab54c3e2c560ffdec15cffb39229ffa17f15ffa17f16ffa17f15ffa17f15ffa17f15ffa17f15ffa17f14ffa17e14ffa07e14ff9f7d13ffae8d23ffd3b44bffd6b64cffb99e41c51512071f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002120f0820c6ac56c3e4c663ffe2c461ffdec15dffdcbe59ffdbbd58ffdabc57ffdabb56ffd9bb54ffd8ba53ffd7b952ffd6b851ffd6b74fffd5b64effd5b74effd7b850ffd7b84fffba9f43c51512071f000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000002120f0820c7ae58c3e5c865ffe3c663ffdfc25effddbf5bffdcbe5affdbbd58ffdabc57ffdabb56ffd9bb55ffd8ba53ffd7b952ffd6b851ffd6b750ffd6b850ffd8ba52ffd8ba51ffbca145c51512081f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100820c8af5ac3e7ca68ffe3c563ffb3932bffa07e14ffa17f15ffa17f15ffa17f15ffa17f15ffa07e14ffa07e14ffa07e14ffa07e14ff9f7d12ffaf8e24ffd8b952ffdabb53ffbda248c51512081f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100820cab15cc3e8cb6affe4c766ffbb9b34ffa98820ffaa8920ffaa8920ffaa881fffa9881fffa9881fffa9871effa9871effa8871effa7861cffb6952dffd9bb54ffdbbd56ffbea449c51512081f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100820cbb25ec3eacd6cffe8cb6affe6ca68ffe5c866ffe4c765ffe3c664ffe2c562ffe2c461ffe1c360ffe0c25effdfc15dffdec15cffddc05affddbf5affddbf59ffddbf58ffbfa54bc51512081f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100920ccb460c3ebcf6effe9cd6cffe2c563ffddc05dffddbf5cffdcbe5bffdbbd5affdabc59ffdabc58ffd9bb57ffd8ba55ffd7b954ffd6b853ffd9bb55ffdec05bffdec05affc1a64dc51613091f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100920cdb562c3edd071ffe8cb6bffb19029ff9b780eff9c7a10ff9c790fff9c790fff9c790fff9b790fff9b790fff9b790fff9b790fff9a780dffad8c23ffddbf5affe0c25dffc2a84fc51613091f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100920cfb664c3eed273ffebce6fffc5a641ffb4942dffb5942effb5942dffb4942dffb4932cffb4932cffb3932bffb3922bffb3922affb19129ffbf9f38ffe0c25effe1c45fffc3a951c51613091f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000212100920d0b866c3efd375ffeed273ffedd172ffecd071ffebcf6fffeace6effeacd6dffe9cc6bffe8cb6affe7ca69ffe6c968ffe5c866ffe4c765ffe4c764ffe3c562ffe3c561ffc5ab53c51613091f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000213100920d1b968c3f1d577ffefd376ffeed374ffedd173ffedd072ffecd070ffebcf6fffeace6effe9cd6cffe8cc6bffe8cb6affe7ca68ffe6c967ffe5c866ffe4c764ffe4c763ffc6ac56c51613091f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000213110a20d3bb6bc3f2d77afff0d477ffedd274ffefd375ffeed274ffecd071ffebce6fffeccf70ffebce6fffe8cb6bffe8cb6affe8cc6bffe7cb6affe4c766ffe5c866ffe6c966ffc7ae58c517140a1f00000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000114120a1ad7bf6ebff4d87cffc7a845ffb4942dffe8cc6dffeed374ffbe9f3affb89832ffe9cd6dffe8cc6cffb79630ffbc9c36ffe9cc6bffe1c462ffb19028ffc1a13bffe7ca68ffcbb15bc017140a190000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ac2ac6573ddc46fc9a2811cf1947107fdc9ae54d3d6bc66cb9c7a13f697750cfaceb35acfceb35acf97750cfa9b7911f6d1b65dcbc5a94dd3947107fd9f7e18f1d2b75dc9b7a053730000000a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000021e1b110941391d198767069e8d6b05d165500e37483c1720896905b28b6a05c35847112a5847112a8b6a05c3896905b1473b1520654f0d378d6b05d18667069d3f3618191c190e09000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b68a060073580412775a041e4c390202ffff2c0074590416765a041a0f0b0001130f0001765a041a75590416ffff1d004c3a0202775a041e73580412aa8106000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fffffffffffffffffc00003ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ff800001ffc88113fffffffffffffffffffffffff"
		bytedata = bytes.fromhex(icohexdata)
		with open(f"{setf}\\Content\\notepad.ico", "wb") as ico:
			ico.write(bytedata)
	if not(jsfc):setup()
	settxt = open(f"{setf}\\settings.json", "r", encoding = "utf-8")
	try:
		setjs = json.load(settxt)
	except:
		settxt.close()
		setup()
		jsonload()
	try:
		if setjs["version"] < version:
			update()
		elif setjs["version"] > version:
			setup()
	except:
		setup()
		jsonload()
	settxt.close()
	si = subprocess.STARTUPINFO()
	si.dwFlags = subprocess.STARTF_USESHOWWINDOW
	runcheck = False
	cmdpid = None
	procid = 0
	try:
		encode = setjs["gui"]["encode"]
		root = tk.Tk()
		app = txtedit(fps_limit=setjs["gui"]["fps"]["limit"], master = root)
		app.mainloop()
		time.sleep(0.5)
		txtedit.killrun()
	except Exception as e:
		try:
			root.destroy()
		except:
			pass
		try:
			restartli = ["Do you want to restart?", "再起動しますか？"]
			restartyn = msg.askretrycancel(title = langmsg[setjs["gui"]["lang"]][8], message = langmsg[setjs["gui"]["lang"]][9] + f"\nError Code>>>{str(e.__class__.__name__)}", detail=f"{str(e)}\n" + restartli[setjs["gui"]["lang"]], icon=msg.ERROR)
		except:
			msg.showerror(title = "Error(エラー)", message = f"Could not load language settings.(言語設定を読み込めませんでした)\nError Code>>>{str(e.__class__.__name__)}\n{str(e)}")
			setup()
			restartyn = False
		restartli = ["Do you want to regenerate the settings.json?", "設定ファイルを再生成しますか？"]
		regenate = msg.askyesno(message=restartli[setjs["gui"]["lang"]])
		if regenate:setup()
		if restartyn:
			if os.path.splitext(selfname)[1] == ".exe":Process(target = txtedit.newwinexeprocess, args=(selfname,)).start()
			elif os.path.splitext(selfname)[1] == ".py" or os.path.splitext(selfname)[1] == ".pyw":Process(target = txtedit.newwinprocess, args=(selfname,)).start()
	finally:
		signal.signal(signal.SIGTERM, signal.SIG_IGN)
		signal.signal(signal.SIGINT, signal.SIG_IGN)
		clean_up()
		signal.signal(signal.SIGTERM, signal.SIG_DFL)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
elif __name__ == "__main__":
	msg.showwarning(message = f"Windows OSのみのサポート\nOS: {platform.system()}")
"""
不具合一覧
	ファイルを開いて変更が保存されているときに言語設定を変更すると、稀に再起動されない問題

version:Beta.2.7.4-02
"""