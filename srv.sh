while true
do
killall python
sleep 1s
killall python #Чтоб наверняка
sleep 60s # Ждём, чтобы не было ошибки при перезапуске "данный порт уже используется"

nohup python srv_main.py &
sleep 6h
done
