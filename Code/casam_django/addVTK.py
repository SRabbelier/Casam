#!/usr/bin/env python

class WinRegStub(object):
	def __init__(self):
		self.HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
		self.KEY_WRITE = "KEY_WRITE"
		self.REG_SZ = "REG_SZ"
	def OpenKey(self, *args):
		pass
	def OpenKey(self, *args):
		pass
	def SetValueEx(self, *args):
		pass
	def CloseKey(self, *args):
		pass
	def ConnectRegistry(self, *args):
		pass
	def QueryValueEx(self, *args):
		return [None]

try:
	import _winreg
except ImportError:
	_winreg = WinRegStub()
	class WindowsError(object): pass

import os.path

def get_registry_value(reg, key, value_name):
	k = _winreg.OpenKey(reg, key)

	try:
		value = _winreg.QueryValueEx(k, value_name)[0]
	except WindowsError, e:
		value = ""

	_winreg.CloseKey(k)
	return value

def set_registry_value(reg, key, value_name, value):
	k = _winreg.OpenKey(reg, key, 0, _winreg.KEY_WRITE)
	value_type = _winreg.REG_SZ
	_winreg.SetValueEx(k, value_name, 0, value_type, value)
	_winreg.CloseKey(k)

def appendPath(path, dir):
	if path:
		if path.find(dir) >= 0:
			return

		path += ";"
	else:
		path = ""

	path += dir
	return path

def main():
	dir = os.path.abspath(os.path.join(os.path.abspath(os.path.curdir), "..", "VTK", "bin"))
	print dir
	reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
	key = r"Environment"
	path = get_registry_value(reg, key, "PATH")
	path = appendPath(path, dir)
	if path:
		set_registry_value(reg, key, "PATH", path)

if __name__ == '__main__':
	main()
