# yubioath-krunner

Displays your YubiKey OATH credentials in krunner when you search for them. Hit enter (or click) to copy the code.

Hacked this together in a couple hours, so PRs or suggestions are welcome.

![](https://i.imgur.com/wrrZR4T.gif)

## Dependencies

- python (3)
- python-configargparse
- python-dbus
- python-fuzzywuzzy
- python-gobject
- python-levenshtein
- libnotify
- yubikey-manager (ykman)
- xclip
- xdotool

## Installation

Available on the [AUR](https://aur.archlinux.org/packages/yubioath-krunner).

Or, on anything else:

```bash
./install.sh
```

## Usage

Simply search for the account name, then hit enter (or click) to copy the code.

The code can also be typed automatically in the active window by setting `type: True` and `copy: False` in the configuration file.

You can also set a prefix word in the configuration file, used to trigger YubiOATH search. This can be useful if you don't want to clutter the krunner menu.

**Hot tip:** If you've added a new account, just copy a code from any account to refresh the credential list.

**Wayland users:** If you are using Wayland, this script probably won't work because it requires xclip and xdotool.

## Configuration file

Located at `~/.config/yubioath-krunner/config` per-user, or system-wide at `/etc/yubioath-krunner/config`

### Default config

```
# Prefix that needs to be typed to trigger YubiKey code search
# For example, you can set it to "mfa" to trigger when you search "mfa google"
# prefix: mfa

# Enable or disable copying codes to the clipboard
copy: True

# Enable or disable typing codes directly into the active window
type: False
```
