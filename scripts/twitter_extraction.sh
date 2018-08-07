echo 'Definindo variáveis'

export DIR=../src/
export SCRIPT=twitter_extractor.py
export AUTH_FILE=../../tw_auth.k
export VENV_DIR=../venv/bin

#source no virtualenv
echo 'Activating virtualenv'
source $VENV_DIR/activate

#japao
echo 'Getting #japao'
python $DIR/$SCRIPT '#japao' -a=$AUTH_FILE -c=100

#japan
echo 'Getting #japan'
python $DIR/$SCRIPT '#japan' -a=$AUTH_FILE -c=100

#japao2020
echo 'Getting #japao2020'
python $DIR/$SCRIPT '#japao2020' -a=$AUTH_FILE -c=100

#japan2020
echo 'Getting #japan2020'
python $DIR/$SCRIPT '#japan2020' -a=$AUTH_FILE -c=100

#jogosolimpicos
echo 'Getting #jogosolimpicos'
python $DIR/$SCRIPT '#jogosolimpicos' -a=$AUTH_FILE -c=100

#olimpiadas
echo 'Getting #olimpiadas'
python $DIR/$SCRIPT '#olimpiadas' -a=$AUTH_FILE -c=100

#olimpiadas2020
echo 'Getting #olimpiadas2020'
python $DIR/$SCRIPT '#olimpiadas2020' -a=$AUTH_FILE -c=100

#olympics
echo 'Getting #olympics'
python $DIR/$SCRIPT '#olympics' -a=$AUTH_FILE -c=100

#tokyo2020
echo 'Getting #tokyo2020'
python $DIR/$SCRIPT '#tokyo2020' -a=$AUTH_FILE -c=100

#tokyo
echo 'Getting #tokyo'
python $DIR/$SCRIPT '#tokyo' -a=$AUTH_FILE -c=100

echo 'deactivating virtualenv'
deactivate;
