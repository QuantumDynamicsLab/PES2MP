# installing anaconda

# download anaconda installer file from website
# change this based on latest conda release (find on anaconda website linux installation)
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh

# installation
bash Anaconda3-2024.10-1-Linux-x86_64.sh

apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

# run the next command in new terminal to enable conda automatically (optional: can be set during conda installation)
# conda config --set auto_activate_base True
