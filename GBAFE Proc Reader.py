#!/usr/bin/python3

#By Teraspark
import argparse
from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox

def isValidFile(file):
	if not file:
		return False
	return file.is_file()

def askForFileIn(filedata=()):
	filedata += (("all files","*.*"),)
	file = askopenfilename(title="Open",filetypes=filedata,defaultextension=filedata)
	return Path(file)

def askForFileOut(filedata=()):
	filedata += (("all files","*.*"),)
	file = asksaveasfilename(title="Save As",filetypes=filedata,defaultextension=filedata)
	return Path(file)

procdefs = """
_6C_END
_6C_SET_NAME(@p)
_6C_CALL_ROUTINE(@p)
_6C_LOOP_ROUTINE(@p)
_6C_SET_DESTRUCTOR(@p)
_6C_NEW_CHILD(@p)
_6C_NEW_CHILD_BLOCKING(@p)
_6C_NEW_MAIN_BUGGED(@p)
_6C_UNIL_EXISTS(@p)
_6C_END_ALL(@p)
_6C_BREAK_ALL_LOOP(@p)
_6C_LABEL(@s2)
_6C_GOTO(@s2)
_6C_JUMP(@p)
_6C_SLEEP(@s2)
_6C_SET_MARK(@s2)
_6C_BLOCK
_6C_END_IF_DUPLICATE
_6C_SET_BIT4
_6C_13
_6C_WHILE_ROUTINE(@p)
_6C_15
_6C_CALL_ROUTINE_2(@p)
_6C_END_DUPLICATES
_6C_CALL_ROUTINE_ARG(@p, @s2)
_6C_19
""".split('\n')
procdefs = list(filter(None,procdefs))

class procfile():
	file = None
	address = 0
	def readproc(self):
		proc = ''
		if (self.address < 0):
			return '' # return blank string if invalid address
		#stuff for reading the proc
		proc = "ORG " + hex(self.address) + '\n'
		with self.file.open(mode='rb') as f:
			f.seek(self.address)
			while(True):
				s1 = int.from_bytes(f.read(2),byteorder='little')
				s2 = int.from_bytes(f.read(2),byteorder='little')
				poin = int.from_bytes(f.read(4),byteorder='little')
				
				try:
					c = procdefs[s1]
					c = c.replace('@p',hex(poin))
					c = c.replace('@s2',hex(s2))
					proc += c + '\n'
				except:
					proc += 'SHORT '+hex(s1)+' '+hex(s2)+'; WORD '+ hex(poin)
					proc += '\t//not a valid proc command\n'
					break
				
				if(not s1):
					break
		return (proc + '\n')
		
	def setFile(self,newfile):
		if isValidFile(newfile):
			self.file = newfile
		return
		
	def setOffset(self,location):
		try:
			self.address = int(location,16)
		except:
			self.address = -1
		return
	
if __name__ == '__main__':
	sfile = procfile()
	
	def LoadInFile():
		newfile = askForFileIn((("GBA file","*.gba"),))
		if isValidFile(newfile):
			filename.configure(text=newfile.name)
			address.set('0')
			sfile.setFile(newfile)
			sfile.setOffset('0')
			clearInfo()
		else:
			prompt = messagebox.showwarning(title="Input File Error", message="selected file is not valid")
		return
	
	def getProcInfo():
		if(not isValidFile(sfile.file)):
			prompt = messagebox.showwarning(title='Error',message="no file to read from detected")
			return
		sfile.setOffset(address.get())
		z = ''
		try:
			z = sfile.readproc()
			outinfo.insert('end',z)
		except:
			prompt = messagebox.showwarning(title="Error",message="could not read")
			# prompt = messagebox.showwarning(title="Offset Error",message="given offset is not valid")
			# return
		# with file.open(mode='rb') as f:
			# f.seek(z)
			# x = f.read(8)
			# outinfo.insert('end',x.hex())
		return
	
	def clearInfo():
		outinfo.delete('1.0','end')
		return
	
	def saveToFile():
		outfile = askForFileOut([("EVENT file","*.event"),("Text file","*.txt")])
		if not (outfile == Path()):
			try:
				output = outinfo.get('1.0','end')
				outfile.write_text(output)
			except:
				prompt = messagebox.showwarning(title="Output Error", message="could not save to file properly")
		return
	
	master = tk.Tk()
	master.title("GBAFE Proc Reader")
	fileframe = tk.Frame(master)
	fileframe.pack(pady=10)
	filename = tk.Label(fileframe,text="Load in a file")
	filename.pack()
	loadfile = tk.Button(fileframe,text="Load File",command=LoadInFile)
	loadfile.pack()
	
	address = tk.StringVar()
	offset = tk.Frame(master)
	offset.pack()
	offLabel = tk.Label(offset, text="Proc Offset")
	offLabel.pack(side = tk.LEFT)
	offHex = tk.Entry(offset,textvariable=address)
	offHex.pack(side = tk.LEFT,padx = 5)
	offButt = tk.Button(offset,command=getProcInfo,text="Find")
	offButt.pack(side = tk.LEFT, padx = 5)
	
	output = tk.Frame(master)
	output.pack(pady=5)
	outLabel = tk.Label(output, text="Proc Info")
	outLabel.pack()
	outclear = tk.Button(output, text="Clear",command=clearInfo)
	outclear.pack()
	outscroll = tk.Scrollbar(output)
	outscroll.pack(side=tk.RIGHT, fill=tk.Y)
	outinfo = tk.Text(output, yscrollcommand=outscroll.set)
	outinfo.pack(pady = 5)
	
	outsave = tk.Button(output, text="Save",command=saveToFile) #remember to add save file command
	outsave.pack(side=tk.BOTTOM,pady = 5)
	master.mainloop()
	
"""
-	not done
+	wip
*	finished

-	change proc defs into a class
	-	read in a language file for how the data is formatted
		-	figure out how to set up termination case (end of data)
	-	add extra button for switching languages
-	set up command line options
-	have error messages handled by a function
"""
