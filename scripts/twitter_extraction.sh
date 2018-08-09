#!/usr/bin/env bash
echo 'Definindo variáveis'

## HOME DA APLICAÇÃO
export DIR=/Users/Marku/Documents/WorkSpace/twitter-collector
export APP_DIR=$DIR/src/twitter_extractor.py
export AUTH_FILE=$DIR/config.ini
## HOME DO VIRTUALENV COM AS DEPENDENCIAS INSTALADAS
export VENV_DIR=$DIR/venv/bin
export LANGUAGE=''

#source no virtualenv
echo 'Activating virtualenv'
source $VENV_DIR/activate

#japao
echo 'Getting #japao'
python $APP_DIR '#japao' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#japan
echo 'Getting #japan'
python $APP_DIR '#japan' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#japao2020
echo 'Getting #japao2020'
python $APP_DIR '#japao2020' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#japan2020
echo 'Getting #japan2020'
python $APP_DIR '#japan2020' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#jogosolimpicos
echo 'Getting #jogosolimpicos'
python $APP_DIR '#jogosolimpicos' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#olimpiadas
echo 'Getting #olimpiadas'
python $APP_DIR '#olimpiadas' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#olimpiadas2020
echo 'Getting #olimpiadas2020'
python $APP_DIR '#olimpiadas2020' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#olympics
echo 'Getting #olympics'
python $APP_DIR '#olympics' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#tokyo2020
echo 'Getting #tokyo2020'
python $APP_DIR '#tokyo2020' -a=$AUTH_FILE -l=$LANGUAGE -c=100

#tokyo
echo 'Getting #tokyo'
python $APP_DIR '#tokyo' -a=$AUTH_FILE -l=$LANGUAGE -c=100

echo 'Data Collected sucessfully'
echo 'deactivating virtualenv'
deactivate;
