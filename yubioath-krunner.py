#!/bin/env python3
from gi.repository import GLib
import dbus.service
import re
from fuzzywuzzy import process
import subprocess
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

objpath="/yubioath"

iface="org.kde.krunner1"
class Runner(dbus.service.Object):
    def __init__(self):
        self.credentials = self.get_credentials()
        dbus.service.Object.__init__(self, dbus.service.BusName("me.odensc.yubioath", dbus.SessionBus()), objpath)

    def get_credentials(self):
        result = subprocess.run(["ykman", "oath", "list"], stdout=subprocess.PIPE)
        return [
            {
                "id": cred,
                "issuer": cred.split(":")[0],
                "account_name": cred.split(":")[1]
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
        subprocess.run("echo -n '{}' | xclip -selection clipboard".format(code), shell=True)
        subprocess.run(["notify-send", "--urgency=low", "--expire-time=2000", "--icon=nm-vpn-active-lock", "YubiOATH", "Code copied to clipboard"])
        # Refresh credentials.
        self.credentials = self.get_credentials()

        return

runner = Runner()
loop = GLib.MainLoop()
loop.run()
