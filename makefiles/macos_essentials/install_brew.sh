/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

cd /opt/homebrew/bin/

PATH=$PATH:/opt/homebrew/bin

echo export PATH=$PATH:/opt/homebrew/bin >> ~/.zshrc