echo "CREATE ENV"
conda create -p venv python=3.10 -y 
echo "ACTIVATE ENV"
conda activate ./venv
echo "DOWNLOAD REQUIREMENTS"
pip install -r requirements.txt
echo "FINSH DOWNLOAD REQUIREMENTS"
