import colorsys
import wifileds
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
from Screens.Screen import Screen
from Components.Label import Label
from Components.Sources.List import List
from Components.config import *
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from os import system, remove
from Components.Sources.CanvasSource import CanvasSource
def RGB(r,g,b):
	return (r<<16)|(g<<8)|b
config.plugins.milight = ConfigSubsection()
config.plugins.milight.boblight = ConfigYesNo(default=False)
config.plugins.milight.select = ConfigSelection(default = "ip", choices = [("ip", _("IP&other config")),("allzones", _("All zones")),("zone1", _("Zone 1")),("zone2", _("Zone 2")),("zone3", _("Zone 3")),("zone4", _("Zone 4"))])
config.plugins.milight.zoneall_color_r = ConfigSlider(default=255, increment=5, limits=(0,255))
config.plugins.milight.zoneall_color_g = ConfigSlider(default=25, increment=5, limits=(0,255))
config.plugins.milight.zoneall_color_b = ConfigSlider(default=2, increment=5, limits=(0,255))
config.plugins.milight.zoneallbrightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone1_color_r = ConfigSlider(default=255, increment=5, limits=(0,255))
config.plugins.milight.zone1_color_g = ConfigSlider(default=25, increment=5, limits=(0,255))
config.plugins.milight.zone1_color_b = ConfigSlider(default=2, increment=5, limits=(0,255))
config.plugins.milight.zone1brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone2_color_r = ConfigSlider(default=255, increment=5, limits=(0,255))
config.plugins.milight.zone2_color_g = ConfigSlider(default=25, increment=5, limits=(0,255))
config.plugins.milight.zone2_color_b = ConfigSlider(default=2, increment=5, limits=(0,255))
config.plugins.milight.zone2brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone3_color_r = ConfigSlider(default=255, increment=5, limits=(0,255))
config.plugins.milight.zone3_color_g = ConfigSlider(default=25, increment=5, limits=(0,255))
config.plugins.milight.zone3_color_b = ConfigSlider(default=2, increment=5, limits=(0,255))
config.plugins.milight.zone3brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone4_color_r = ConfigSlider(default=255, increment=5, limits=(0,255))
config.plugins.milight.zone4_color_g = ConfigSlider(default=25, increment=5, limits=(0,255))
config.plugins.milight.zone4_color_b = ConfigSlider(default=2, increment=5, limits=(0,255))
config.plugins.milight.zone4brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.ip = ConfigIP(default=[192,168,2,106])
config.plugins.milight.port = ConfigInteger(default=8899, limits=(1, 9999))
class HDMU_MilightControl(Screen, ConfigListScreen):
	def __init__(self, session):
		Screen.__init__(self, session)
		skin = """<screen name="HDMU_MilightControl" position="center,center" size="720,605" title="Milight Control" flags="wfNoBorder" backgroundColor="#000">
				<eLabel position="0,0" zPosition="-3" size="720,605" backgroundColor="black" />
				<eLabel position="50,50" zPosition="-1" size="620,505" backgroundColor="black" />
				<widget name="config" zPosition="2" position="center,center" size="400,300" scrollbarMode="showOnDemand" foregroundColor="white" backgroundColor="black" transparent="1"/>
				<ePixmap position="250,530" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_red.png" alphatest="blend"/>
				<ePixmap position="250,571" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_green.png" alphatest="blend"/>
				<ePixmap position="450,530" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_yellow.png" alphatest="blend"/>
				<ePixmap position="450,571" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_blue.png" alphatest="blend"/>
				<widget name="red" zPosition="2" halign="left" position="300,530" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="green" zPosition="2" halign="left" position="300,571" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="yellow" zPosition="2" halign="left" position="500,530" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="blue" zPosition="2" halign="left" position="500,571" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="r" zPosition="2" halign="right" position="460,182" size="150,80" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;21"/>
				<widget name="rstat" zPosition="2" halign="right" position="505,182" size="150,80" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;21"/>
				<widget source="Canvas" render="Canvas" position="25,25" zPosition="-2" size="670,550" transparent="1"/>
			</screen>"""
		self.skin = skin
		self["green"] = Label(_("All zones on"))
		self["red"] = Label(_("All zones off"))
		self["yellow"] = Label(_("All zones min brightness"))
		self["blue"] = Label(_("All zones max brightness"))
		self["Canvas"] = CanvasSource()
		if config.plugins.milight.select.value == "allzones":
			r = config.plugins.milight.zoneall_color_r.value
			g = config.plugins.milight.zoneall_color_g.value
			b = config.plugins.milight.zoneall_color_b.value
		elif config.plugins.milight.select.value == "zone1":
			r = config.plugins.milight.zone1_color_r.value
			g = config.plugins.milight.zone1_color_g.value
			b = config.plugins.milight.zone1_color_b.value
		elif config.plugins.milight.select.value == "zone2":
			r = config.plugins.milight.zone2_color_r.value
			g = config.plugins.milight.zone2_color_g.value
			b = config.plugins.milight.zone2_color_b.value
		elif config.plugins.milight.select.value == "zone3":
			r = config.plugins.milight.zone3_color_r.value
			g = config.plugins.milight.zone3_color_g.value
			b = config.plugins.milight.zone3_color_b.value
		elif config.plugins.milight.select.value == "zone4":
			r = config.plugins.milight.zone4_color_r.value
			g = config.plugins.milight.zone4_color_g.value
			b = config.plugins.milight.zone4_color_b.value
		else:
			r = 0
			g = 0
			b = 0
		self["r"] = Label(str(r) +"\n"+ str(g) +"\n"+ str(b))
		self["rstat"] = Label("/255\n/255\n/255")
		if config.plugins.milight.select.value == "ip":
			self["r"].hide()
			self["rstat"].hide()
		self["Canvas"].fill(0, 0, 720, 605, RGB(r,g,b))
		self["Canvas"].flush()
		self.ip = '%d.%d.%d.%d' % tuple(config.plugins.milight.ip.value)
		self.led_connection = wifileds.limitlessled.connect(self.ip, int(config.plugins.milight.port.value))
		self.list = [ ]
		self.onChangedEntry = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "NumberActions"],
		{
			"cancel": self.exit,
			"ok": self.OK,
			"left": self.keyLeft,
			"right": self.keyRight,
			"green": self.allon,
			"red": self.alloff,
			"yellow": self.minbright,
			"blue": self.maxbright,
		}, -1)
		self.createsetup()
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()
	def exit(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()
	def createsetup(self):
		if config.plugins.milight.select.value == "ip":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_('IP:'), config.plugins.milight.ip),
				getConfigListEntry(_('Port:'), config.plugins.milight.port),
				getConfigListEntry(_('Enable Boblight:'), config.plugins.milight.boblight),
			]
			self["r"].hide()
			self["rstat"].hide()
		elif config.plugins.milight.select.value == "allzones":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_("All Zone red color:"), config.plugins.milight.zoneall_color_r),
				getConfigListEntry(_("All Zone green color:"), config.plugins.milight.zoneall_color_g),
				getConfigListEntry(_("All Zone blue color:"), config.plugins.milight.zoneall_color_b),
				getConfigListEntry(_("All Zone Brightness:"), config.plugins.milight.zoneallbrightness),
			]
		elif config.plugins.milight.select.value == "zone1":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_("Zone 1 red color:"), config.plugins.milight.zone1_color_r),
				getConfigListEntry(_("Zone 1 green color:"), config.plugins.milight.zone1_color_g),
				getConfigListEntry(_("Zone 1 blue color:"), config.plugins.milight.zone1_color_b),
				getConfigListEntry(_("Zone 1 Brightness:"), config.plugins.milight.zone1brightness),
			]
		elif config.plugins.milight.select.value == "zone2":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_("Zone 2 red color:"), config.plugins.milight.zone2_color_r),
				getConfigListEntry(_("Zone 2 green color:"), config.plugins.milight.zone2_color_g),
				getConfigListEntry(_("Zone 2 blue color:"), config.plugins.milight.zone2_color_b),
				getConfigListEntry(_("Zone 2 Brightness:"), config.plugins.milight.zone2brightness),
			]
		elif config.plugins.milight.select.value == "zone3":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_("Zone 3 red color:"), config.plugins.milight.zone3_color_r),
				getConfigListEntry(_("Zone 3 green color:"), config.plugins.milight.zone3_color_g),
				getConfigListEntry(_("Zone 3 blue color:"), config.plugins.milight.zone3_color_b),
				getConfigListEntry(_("Zone 3 Brightness:"), config.plugins.milight.zone3brightness),
			]
		elif config.plugins.milight.select.value == "zone4":
			list = [
				getConfigListEntry(_('Select config:'), config.plugins.milight.select),
				getConfigListEntry(_("Zone 4 red color:"), config.plugins.milight.zone4_color_r),
				getConfigListEntry(_("Zone 4 green color:"), config.plugins.milight.zone4_color_g),
				getConfigListEntry(_("Zone 4 blue color:"), config.plugins.milight.zone4_color_b),
				getConfigListEntry(_("Zone 4 Brightness:"), config.plugins.milight.zone4brightness),
			]
		self["config"].list = list
		self["config"].setList(list)
	def keyLeft(self):
		self["config"].handleKey(KEY_LEFT)
		if self["config"].getCurrent()[1] == config.plugins.milight.select:
			self.up()
			self.createsetup()
		elif self["config"].getCurrent()[1] == config.plugins.milight.boblight:
			self.boblight()
		elif self["config"].getCurrent()[1] in (config.plugins.milight.ip, config.plugins.milight.port):
			self.ip = '%d.%d.%d.%d' % tuple(config.plugins.milight.ip.value)
			self.led_connection = wifileds.limitlessled.connect(self.ip, int(config.plugins.milight.port.value))
		else:
			self.update()
	def keyRight(self):
		self["config"].handleKey(KEY_RIGHT)
		if self["config"].getCurrent()[1] == config.plugins.milight.select:
			self.up()
			self.createsetup()
		elif self["config"].getCurrent()[1] == config.plugins.milight.boblight:
			self.boblight()
		elif self["config"].getCurrent()[1] in (config.plugins.milight.ip, config.plugins.milight.port):
			self.ip = '%d.%d.%d.%d' % tuple(config.plugins.milight.ip.value)
			self.led_connection = wifileds.limitlessled.connect(self.ip, int(config.plugins.milight.port.value))
		else:
			self.update()
	def boblight(self):
		if config.plugins.milight.boblight.value is True:
			if fileExists("/etc/.milight.lock"):
				return
			else:
				system("touch /etc/.milight.lock")
		else:
			if fileExists("/etc/.milight.lock"):
				remove("/etc/.milight.lock")
	def up(self):
		self["r"].show()
		self["rstat"].show()
		r = [ ]
		g = [ ]
		b = [ ]
		if config.plugins.milight.select.value == "allzones":
			r = config.plugins.milight.zoneall_color_r.value
			g = config.plugins.milight.zoneall_color_g.value
			b = config.plugins.milight.zoneall_color_b.value
		elif config.plugins.milight.select.value == "zone1":
			r = config.plugins.milight.zone1_color_r.value
			g = config.plugins.milight.zone1_color_g.value
			b = config.plugins.milight.zone1_color_b.value
		elif config.plugins.milight.select.value == "zone2":
			r = config.plugins.milight.zone2_color_r.value
			g = config.plugins.milight.zone2_color_g.value
			b = config.plugins.milight.zone2_color_b.value
		elif config.plugins.milight.select.value == "zone3":
			r = config.plugins.milight.zone3_color_r.value
			g = config.plugins.milight.zone3_color_g.value
			b = config.plugins.milight.zone3_color_b.value
		elif config.plugins.milight.select.value == "zone4":
			r = config.plugins.milight.zone4_color_r.value
			g = config.plugins.milight.zone4_color_g.value
			b = config.plugins.milight.zone4_color_b.value
		else:
			r = 0
			g = 0
			b = 0
		self["r"].setText(str(r) +"\n"+ str(g) +"\n"+ str(b))
		self["Canvas"].fill(0, 0, 720, 605, RGB(r,g,b))
		self["Canvas"].flush()
	def update(self):
		if self["config"].getCurrent()[1] == config.plugins.milight.zoneallbrightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zoneallbrightness.value)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone1brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 1)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone2brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone2brightness.value, 2)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone3brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone3brightness.value, 3)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone4brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone4brightness.value, 4)
		else:
			if self["config"].getCurrent()[1] in (config.plugins.milight.zoneall_color_r, config.plugins.milight.zoneall_color_g, config.plugins.milight.zoneall_color_b):
				r = config.plugins.milight.zoneall_color_r.value
				g = config.plugins.milight.zoneall_color_g.value
				b = config.plugins.milight.zoneall_color_b.value
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone1_color_r, config.plugins.milight.zone1_color_g, config.plugins.milight.zone1_color_b):
				r = config.plugins.milight.zone1_color_r.value
				g = config.plugins.milight.zone1_color_g.value
				b = config.plugins.milight.zone1_color_b.value
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone2_color_r, config.plugins.milight.zone2_color_g, config.plugins.milight.zone2_color_b):
				r = config.plugins.milight.zone2_color_r.value
				g = config.plugins.milight.zone2_color_g.value
				b = config.plugins.milight.zone2_color_b.value
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone3_color_r, config.plugins.milight.zone3_color_g, config.plugins.milight.zone3_color_b):
				r = config.plugins.milight.zone3_color_r.value
				g = config.plugins.milight.zone3_color_g.value
				b = config.plugins.milight.zone3_color_b.value
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone4_color_r, config.plugins.milight.zone4_color_g, config.plugins.milight.zone4_color_b):
				r = config.plugins.milight.zone4_color_r.value
				g = config.plugins.milight.zone4_color_g.value
				b = config.plugins.milight.zone4_color_b.value
			h, l, s = colorsys.rgb_to_hls(float(r)/255.0,float(g)/255.0,float(b)/255.0)
			h=int(int(h * 360) + 120)
			if h>=360:
				h = h - 360
			h=abs(h-360)
			h = int((h / 360.0) * 255.0)
			self["r"].setText(str(r) +"\n"+ str(g) +"\n"+ str(b))
			self["Canvas"].fill(0, 0, 720, 605, RGB(r,g,b))
			self["Canvas"].flush()
			if self["config"].getCurrent()[1] in (config.plugins.milight.zoneall_color_r, config.plugins.milight.zoneall_color_g, config.plugins.milight.zoneall_color_b):
				if r == 255 and g == 255 and b == 255:
					self.led_connection.rgbw.white()
					self.led_connection.rgbw.set_brightness(config.plugins.milight.zoneallbrightness.value)
				elif r == 0 and g == 0 and b == 0:
					self.led_connection.rgbw.all_off()
				else:
					self.led_connection.rgbw.set_color_hex(chr(h))
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone1_color_r, config.plugins.milight.zone1_color_g, config.plugins.milight.zone1_color_b):
				if r == 255 and g == 255 and b == 255:
					self.led_connection.rgbw.white(1)
					self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 1)
				elif r == 0 and g == 0 and b == 0:
					self.led_connection.rgbw.zone_off(1)
				else:
					self.led_connection.rgbw.set_color_hex(chr(h), 1)
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone2_color_r, config.plugins.milight.zone2_color_g, config.plugins.milight.zone2_color_b):
				if r == 255 and g == 255 and b == 255:
					self.led_connection.rgbw.white(2)
					self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 2)
				elif r == 0 and g == 0 and b == 0:
					self.led_connection.rgbw.zone_off(2)
				else:
					self.led_connection.rgbw.set_color_hex(chr(h), 2)
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone3_color_r, config.plugins.milight.zone3_color_g, config.plugins.milight.zone3_color_b):
				if r == 255 and g == 255 and b == 255:
					self.led_connection.rgbw.white(3)
					self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 3)
				elif r == 0 and g == 0 and b == 0:
					self.led_connection.rgbw.zone_off(3)
				else:
					self.led_connection.rgbw.set_color_hex(chr(h), 3)
			elif self["config"].getCurrent()[1] in (config.plugins.milight.zone4_color_r, config.plugins.milight.zone4_color_g, config.plugins.milight.zone4_color_b):
				if r == 255 and g == 255 and b == 255:
					self.led_connection.rgbw.white(4)
					self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 4)
				elif r == 0 and g == 0 and b == 0:
					self.led_connection.rgbw.zone_off(4)
				else:
					self.led_connection.rgbw.set_color_hex(chr(h), 4)
	def alloff(self):
		self.led_connection.rgbw.all_off()
	def allon(self):
		self.led_connection.rgbw.white()
		self.led_connection.rgbw.all_on()
	def minbright(self):
		self.led_connection.rgbw.min_brightness()
	def maxbright(self):
		self.led_connection.rgbw.max_brightness()
	def OK(self):
		for x in self["config"].list:
			x[1].save()
		self.close()
def menu(session, **kwargs):
	session.open(HDMU_MilightControl)
def Plugins(**kwargs):
	return [PluginDescriptor(name = "MiLight Control", description = "Control your MiLight", where = [PluginDescriptor.WHERE_PLUGINMENU], fnc = menu),]
