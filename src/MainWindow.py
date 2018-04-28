#!/usr/bin/env python3

# standard library
import configparser
import os

# third-party library
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# imports from current project
from config import CONFIG_FILE
from config import ICONS



class MainWindow(Gtk.ApplicationWindow):
    """Main class for the GUI.

    This class displays the main window that the user will
    see when he wants to manage Battery Monitor
    """

    def __init__(self) -> None:
        Gtk.Window.__init__(self, title='Battery Monitor')
        self.set_default_size(800, 400)
        self.set_resizable(True)
        self.set_border_width(0)
        self.get_focus()
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(ICONS['app'])
        self.config_dir = os.path.dirname(CONFIG_FILE)
        self.config = configparser.ConfigParser()
        self.load_config()

        label0 = Gtk.Label('Very Low Battery Warning at')
        label0.set_justify(Gtk.Justification.LEFT)
        label0.set_halign(Gtk.Align.START)
        label0.set_hexpand(True)
        label1 = Gtk.Label('Low Battery Warning at')
        label1.set_justify(Gtk.Justification.LEFT)
        label1.set_halign(Gtk.Align.START)
        label1.set_hexpand(True)
        label2 = Gtk.Label('Third Custom Warning at')
        label2.set_justify(Gtk.Justification.LEFT)
        label2.set_halign(Gtk.Align.START)
        label2.set_hexpand(True)
        label3 = Gtk.Label('Second Custom Warning at')
        label3.set_justify(Gtk.Justification.LEFT)
        label3.set_halign(Gtk.Align.START)
        label3.set_hexpand(True)
        label4 = Gtk.Label('First Custom Warning at')
        label4.set_justify(Gtk.Justification.LEFT)
        label4.set_halign(Gtk.Align.START)
        label4.set_hexpand(True)
        label5 = Gtk.Label('Notification Stability')
        label5.set_justify(Gtk.Justification.LEFT)
        label5.set_halign(Gtk.Align.START)
        label5.set_hexpand(True)

        self.entry0 = Gtk.Entry()
        self.entry0.set_text(str(self.critical_battery))
        self.entry0.set_tooltip_text('Set in percentage')
        self.entry1 = Gtk.Entry()
        self.entry1.set_text(str(self.low_battery))
        self.entry1.set_tooltip_text('Set in percentage')
        self.entry2 = Gtk.Entry()
        self.entry2.set_text(str(self.third_custom_warning))
        self.entry2.set_tooltip_text('Set in percentage, must be smaller than Other Warnings')
        self.entry3 = Gtk.Entry()
        self.entry3.set_text(str(self.second_custom_warning))
        self.entry3.set_tooltip_text('Set in percentage, , must be greater than Third Custom Warning')
        self.entry4 = Gtk.Entry()
        self.entry4.set_text(str(self.first_custom_warning))
        self.entry4.set_tooltip_text('Set in percentage, must be greater than Second Custom Warning')
        self.entry5 = Gtk.Entry()
        self.entry5.set_text(str(self.notification_stability))
        self.entry5.set_tooltip_text('Set in second')

        save_button = Gtk.Button(label='Save')
        save_button.connect('clicked', self.save_config)

        grid = Gtk.Grid()
        self.add(grid)
        grid.set_row_spacing(15)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        grid.set_border_width(10)
        grid.set_column_spacing(2)
        grid.set_column_homogeneous(False)
        grid.attach(label0, 0, 0, 14, 1)
        grid.attach(self.entry0, 14, 0, 1, 1)
        grid.attach(label1, 0, 1, 14, 1)
        grid.attach(self.entry1, 14, 1, 1, 1)
        grid.attach(label2, 0, 2, 14, 1)
        grid.attach(self.entry2, 14, 2, 1, 1)
        grid.attach(label3, 0, 3, 14, 1)
        grid.attach(self.entry3, 14, 3, 1, 1)
        grid.attach(label4, 0, 4, 14, 1)
        grid.attach(self.entry4, 14, 4, 1, 1)
        grid.attach(label5, 0, 5, 14, 1)
        grid.attach(self.entry5, 14, 5, 1, 1)
        grid.attach(save_button, 9, 7, 1, 1)

    def load_config(self):
        """Loads configurations from config file.

        Tries to read and parse from config file. If the config file is missing or not readable, then it triggers default configurations.
        """

        try:
            self.config.read(CONFIG_FILE)
            self.critical_battery = self.config['settings']['critical_battery']
            self.low_battery = self.config['settings']['low_battery']
            self.first_custom_warning = self.config['settings']['first_custom_warning']
            self.second_custom_warning = self.config['settings']['second_custom_warning']
            self.third_custom_warning = self.config['settings']['third_custom_warning']
            self.notification_stability = self.config['settings']['notification_stability']
        except:
            print('Config file is missing or not readable. Using default configurations.')
            self.critical_battery = '10'
            self.low_battery = '30'
            self.first_custom_warning = ''
            self.second_custom_warning = ''
            self.third_custom_warning = ''
            self.notification_stability = '5'

    def save_config(self, widget):
        """Saves configurations to config file.

        Saves user-defined configurations to config file. If the config file does not exist, it creates a new config file (~/.config/battery-monitor/battery-monitor.cfg) in user's home directory.
        """

        if os.path.exists(self.config_dir):
            pass
        else:
            os.makedirs(self.config_dir)
        self.config['settings'] = {
            'critical_battery': self.entry0.get_text(),
            'low_battery': self.entry1.get_text(),
            'third_custom_warning': self.entry2.get_text(),
            'second_custom_warning': self.entry3.get_text(),
            'first_custom_warning': self.entry4.get_text(),
            'notification_stability': self.entry5.get_text()
        }
        with open(CONFIG_FILE, 'w') as f:
            self.config.write(f)
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK,
                                       "Successfully Saved!")
            dialog.format_secondary_text(
                'You settings have been saved successfully.')
            dialog.run()
            print("Info dialog closed")
            dialog.destroy()