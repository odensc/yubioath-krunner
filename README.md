# yubioath-krunner

Displays your YubiKey OATH credentials in krunner when you search for them. Hit enter (or click) to copy the code.

Hacked this together in a couple hours, so PRs or suggestions are welcome.

![](https://i.imgur.com/wrrZR4T.gif)

## Dependencies

* python3
* python3-dbus
* python3-fuzzywuzzy
* python3-gobject
* python3-levenshtein
* libnotify
* yubikey-manager (ykman)
* xclip
* xdotool

## Installation

Available on the [AUR](https://aur.archlinux.org/packages/yubioath-krunner).

Or, on anything else:

```bash
./install.sh
```

## Usage

Simply search for the account name, then hit enter (or click) to copy the code.
Code can also be typed automatically in the active window by set `type: True` and `copy: False` in the user specific config file ~/.config/yubioath-krunner/settings.cfg
or system wide in /etc/yubioath-krunner/settings.cfg

You can also set a prefix word in the settings.cfg to trigger search. This can be useful if you don't want to clutter krunner search menu

**Hot tip:** If you've added a new account, just copy a code from any account to refresh the credential list.

**Wayland users:** If you are using Wayland, directly typing code with xdotool won't work because it's doesn't support Wayland.
