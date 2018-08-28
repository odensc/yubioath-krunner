PREFIX=${PREFIX:-~/.local}
echo $PREFIX
mkdir -p $PREFIX/share/kservices5
mkdir -p ~/.config/autostart-scripts
cp yubioath-krunner.desktop $PREFIX/share/kservices5
cp yubioath-krunner.py ~/.config/autostart-scripts