#!/usr/bin/env python3

import os
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

conservativeMode = False;

def main():
  indicator = appindicator.Indicator.new("ideapad-tray", "battery", appindicator.IndicatorCategory.APPLICATION_STATUS)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(menu())
  gtk.main()  

def menu():
  global conservativeMode
  conservativeMode = getConservationMode()

  menu = gtk.Menu()

  switch_conservativeMode = gtk.CheckMenuItem("Conservative Mode")
  switch_conservativeMode.set_active(conservativeMode)
  switch_conservativeMode.connect('activate', toggleConservativeMode)
  menu.append(switch_conservativeMode)
  
  exittray = gtk.MenuItem('Exit Tray')
  exittray.connect('activate', quit)
  menu.append(exittray)

  menu.show_all()
  return menu
  
def getConservationMode():
  mode = os.popen('cat /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode').read()
  return bool(mode)
  
def quit(_):
  gtk.main_quit()

def toggleConservativeMode(_):
  global conservativeMode;

  if conservativeMode:
    os.system("echo 0 | sudo tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode")
    conservativeMode = False
  else:
    os.system("echo 1 | sudo tee /sys/bus/platform/drivers/ideapad_acpi/VPC2004:00/conservation_mode")
    conservativeMode = True

if __name__ == "__main__":
  main()
