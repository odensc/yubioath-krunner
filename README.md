# yubioath-krunner

Displays your YubiKey OATH credentials in krunner when you search for them. Hit enter (or click) to copy the code.

Hacked this together in a couple hours, so PRs or suggestions are welcome.

![](https://i.imgur.com/wrrZR4T.gif)

## Dependencies

* python3
* python3-dbus
* python3-fuzzywuzzy
* python3-gobject
* libnotify
* yubikey-manager (ykman)

## Installation

Available on the [AUR](https://aur.archlinux.org/packages/yubioath-krunner).

Or, on anything else:

```bash
./install.sh
```