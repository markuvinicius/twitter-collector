#!/usr/bin/env bash
echo 'Definindo variáveis'

export DIR=/Users/Marku/Documents/WorkSpace/twitter-collector
export SCRIPT=$DIR/src/twitter_extractor.py
export AUTH_FILE=$DIR/config_example.ini
export VENV_DIR=$DIR/venv/bin

#source no virtualenv
#echo 'Activating virtualenv'
#source $VENV_DIR/activate

#japao
echo 'Getting #japao'
python $SCRIPT '#japao' -a=$AUTH_FILE -c=100

#japan
echo 'Getting #japan'
python $SCRIPT '#japan' -a=$AUTH_FILE -c=100

#japao2020
echo 'Getting #japao2020'
python $SCRIPT '#japao2020' -a=$AUTH_FILE -c=100

#japan2020
echo 'Getting #japan2020'
python $SCRIPT '#japan2020' -a=$AUTH_FILE -c=100

#jogosolimpicos
echo 'Getting #jogosolimpicos'
python $SCRIPT '#jogosolimpicos' -a=$AUTH_FILE -c=100

#olimpiadas
echo 'Getting #olimpiadas'
python $SCRIPT '#olimpiadas' -a=$AUTH_FILE -c=100

#olimpiadas2020
echo 'Getting #olimpiadas2020'
python $SCRIPT '#olimpiadas2020' -a=$AUTH_FILE -c=100

#olympics
echo 'Getting #olympics'
python $SCRIPT '#olympics' -a=$AUTH_FILE -c=100

#tokyo2020
echo 'Getting #tokyo2020'
python $SCRIPT '#tokyo2020' -a=$AUTH_FILE -c=100

#tokyo
echo 'Getting #tokyo'
python $SCRIPT '#tokyo' -a=$AUTH_FILE -c=100

echo 'deactivating virtualenv'
#deactivate;
