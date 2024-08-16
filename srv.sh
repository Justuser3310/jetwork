while true
do
killall python
sleep 2s
killall python #Чтоб наверняка

nohup python srv_main.py &
sleep 6h
done
