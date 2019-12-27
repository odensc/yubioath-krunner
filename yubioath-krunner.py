#!/bin/env python3
from gi.repository import GLib
import dbus.service
import re
from fuzzywuzzy import process
import subprocess
from dbus.mainloop.glib import DBusGMainLoop
import configargparse

APP_NAME = "yubioath-krunner"
CONFIG_FILE_NAME = "settings.cfg"

DBusGMainLoop(set_as_default=True)

objpath="/yubioath"

iface="org.kde.krunner1"
class Runner(dbus.service.Object):
    def __init__(self, options):
        self.options = options
        self.credentials = self.get_credentials()
        dbus.service.Object.__init__(self, dbus.service.BusName("me.odensc.yubioath", dbus.SessionBus()), objpath)

    def get_credentials(self):
        result = subprocess.run(["ykman", "oath", "list"], stdout=subprocess.PIPE)
        return [
            {
                "id": cred,
                "issuer": ":" in cred and cred.split(":")[0] or "",
                "account_name": ":" in cred and cred.split(":")[1] or cred
            }
            for cred in result.stdout.decode().split("\n")[:-1]
        ]

    def get_code(self, cred_id):
        result = subprocess.run(["ykman", "oath", "code", cred_id], stdout=subprocess.PIPE)
        code = result.stdout.decode()
        return re.search(" (\d+)$", code).groups()[0]

    @dbus.service.method(iface, out_signature='a(sss)')
    def Actions(self, msg):
        return []

    @dbus.service.method(iface, in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query):
        if query[0:len(self.options.prefix)] == self.options.prefix:
            query = query[len(options.prefix):]
        else:
            return []

        fuzzy_credentials = process.extract(query, [cred["id"] for cred in self.credentials], limit=3)
        results = []

        for y in fuzzy_credentials:
            cred = next(x for x in self.credentials if x["id"] == y[0])
            # Best guess for icon. (todo)
            icon = "nm-vpn-active-lock"
            results.append((cred["id"], cred["issuer"], icon, 100, y[1] / 100, { "subtext": cred["account_name"] }))

        return results

    @dbus.service.method(iface, in_signature='ss')
    def Run(self, matchId, actionId):
        code = self.get_code(matchId)
        if self.options.copy:
            subprocess.run("echo -n '{}' | xclip -selection clipboard".format(code), shell=True)
            subprocess.run(["notify-send", "--urgency=low", "--expire-time=2000", "--icon=nm-vpn-active-lock", "YubiOATH", "Code copyed to clipboard!"])
        if self.options.type:
            subprocess.run(f"xdotool type {code}", shell=True)
            subprocess.run(["notify-send", "--urgency=low", "--expire-time=2000", "--icon=nm-vpn-active-lock", "YubiOATH", "Code typed!"])
        # Refresh credentials.
        self.credentials = self.get_credentials()

        return

config = configargparse.ArgParser(default_config_files=[f'/etc/{APP_NAME}/{CONFIG_FILE_NAME}', f'./{CONFIG_FILE_NAME}', f'~/.config/{APP_NAME}/{CONFIG_FILE_NAME}'])
config.add('--prefix', default="", help='Prefix used to search in krunner')
config.add('--copy', action='store_true', help='Copy code to clipboard')
config.add('--type', action='store_true', help='Type code in active window')
options = config.parse_args()

runner = Runner(options)
loop = GLib.MainLoop()
loop.run()
