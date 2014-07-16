import wifileds
from Plugins.Plugin import PluginDescriptor
from Components.PluginComponent import plugins
from Screens.Screen import Screen
from Components.Label import Label
from Components.Sources.List import List
from Components.config import *
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.ActionMap import ActionMap
config.plugins.milight = ConfigSubsection()
colors = [('off',_("off")),('white',_("white")),('violet',_('violet')),('royal_blue',_('royal_blue')),('baby_blue',_('baby_blue')),('aqua',_('aqua')),('mint',_('mint')),('seafoam_green',_('seafoam_green')),('green',_('green')),('lime_green',_('lime_green')),('yellow',_('yellow')),('yellow_orange',_('yellow_orange')),('orange',_('orange')),('red',_('red')),('pink',_('pink')),('fusia',_('fusia')),('lilac',_('lilac')),('lavendar',_('lavendar'))]
config.plugins.milight.zone1 = ConfigSelection(colors)
config.plugins.milight.zone2 = ConfigSelection(colors)
config.plugins.milight.zone3 = ConfigSelection(colors)
config.plugins.milight.zone4 = ConfigSelection(colors)
config.plugins.milight.zoneall = ConfigSelection(colors)
config.plugins.milight.brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone1brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone2brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone3brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.zone4brightness = ConfigSlider(default=27, limits=(2, 27))
config.plugins.milight.ip = ConfigIP(default=[192,168,2,106])
config.plugins.milight.port = ConfigInteger(default=8899, limits=(1, 9999))
class HDMU_MilightControl(Screen, ConfigListScreen):
	def __init__(self, session):
		Screen.__init__(self, session)
		skin = """<screen name="HDMU_MilightControl" position="280,75" size="720,605" title="Milight Control" flags="wfNoBorder" backgroundColor="#ff000000">
				<eLabel position="0,0" zPosition="-3" size="720,605" backgroundColor="black" />
				<widget name="config" zPosition="2" position="253,215" size="400,300" scrollbarMode="showOnDemand" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<ePixmap position="250,530" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_red.png" alphatest="blend"/>
				<ePixmap position="250,560" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_green.png" alphatest="blend"/>
				<ePixmap position="450,530" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_yellow.png" alphatest="blend"/>
				<ePixmap position="450,560" zPosition="2" size="35,25" pixmap="skin_default/buttons/key_blue.png" alphatest="blend"/>
				<widget name="red" zPosition="2" halign="left" position="300,530" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="green" zPosition="2" halign="left" position="300,560" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="yellow" zPosition="2" halign="left" position="500,530" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
				<widget name="blue" zPosition="2" halign="left" position="500,560" size="150,25" foregroundColor="white" backgroundColor="black" transparent="1" font="Regular;20"/>
			</screen>"""
		self.skin = skin
		self["green"] = Label(_("All zones on"))
		self["red"] = Label(_("All zones off"))
		self["yellow"] = Label(_("All zones min brightness"))
		self["blue"] = Label(_("All zones max brightness"))
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
		list = [
			getConfigListEntry(_('IP'), config.plugins.milight.ip),
			getConfigListEntry(_('Port'), config.plugins.milight.port),
			getConfigListEntry(_("All Zone Color:"), config.plugins.milight.zoneall),
			getConfigListEntry(_("Zone 1 Color:"), config.plugins.milight.zone1),
			getConfigListEntry(_("Zone 2 Color:"), config.plugins.milight.zone2),
			getConfigListEntry(_("Zone 3 Color:"), config.plugins.milight.zone3),
			getConfigListEntry(_("Zone 4 Color:"), config.plugins.milight.zone4),
			getConfigListEntry(_("All Zone Brightness:"), config.plugins.milight.brightness),
			getConfigListEntry(_("Zone 1 Brightness:"), config.plugins.milight.zone1brightness),
			getConfigListEntry(_("Zone 2 Brightness:"), config.plugins.milight.zone2brightness),
			getConfigListEntry(_("Zone 3 Brightness:"), config.plugins.milight.zone3brightness),
			getConfigListEntry(_("Zone 4 Brightness:"), config.plugins.milight.zone4brightness),
		]
		self["config"].list = list
		self["config"].setList(list)
		self.ip = '%d.%d.%d.%d' % tuple(config.plugins.milight.ip.value)
		self.led_connection = wifileds.limitlessled.connect(self.ip, int(config.plugins.milight.port.value))
	def keyLeft(self):
		self["config"].handleKey(KEY_LEFT)
		self.update()
	def keyRight(self):
		self["config"].handleKey(KEY_RIGHT)
		self.update()
	def update(self):
		self.createsetup()
		if self["config"].getCurrent()[1] == config.plugins.milight.brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.brightness.value)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone1brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone1brightness.value, 1)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone2brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone2brightness.value, 2)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone3brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone3brightness.value, 3)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zone4brightness:
			self.led_connection.rgbw.set_brightness(config.plugins.milight.zone4brightness.value, 4)
		elif self["config"].getCurrent()[1] == config.plugins.milight.zoneall:
			if config.plugins.milight.zoneall.value == "white":
				self.led_connection.rgbw.white()
			elif config.plugins.milight.zoneall.value == "off":
				self.led_connection.rgbw.all_off()
			else:
				self.led_connection.rgbw.set_color(config.plugins.milight.zoneall.value)
		else:
			if config.plugins.milight.zone1.value == "white":
				self.led_connection.rgbw.white(1)
			elif config.plugins.milight.zone1.value == "off":
				self.led_connection.rgbw.zone_off(1)
			else:
				self.led_connection.rgbw.set_color(config.plugins.milight.zone1.value, 1)
			if config.plugins.milight.zone2.value == "white":
				self.led_connection.rgbw.white(2)
			elif config.plugins.milight.zone2.value == "off":
				self.led_connection.rgbw.zone_off(2)
			else:
				self.led_connection.rgbw.set_color(config.plugins.milight.zone2.value, 2)
			if config.plugins.milight.zone3.value == "white":
				self.led_connection.rgbw.white(3)
			elif config.plugins.milight.zone3.value == "off":
				self.led_connection.rgbw.zone_off(3)
			else:
				self.led_connection.rgbw.set_color(config.plugins.milight.zone3.value, 3)
			if config.plugins.milight.zone4.value == "white":
				self.led_connection.rgbw.white(4)
			elif config.plugins.milight.zone4.value == "off":
				self.led_connection.rgbw.zone_off(4)
			else:
				self.led_connection.rgbw.set_color(config.plugins.milight.zone4.value, 4)
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