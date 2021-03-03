cd app/
# Start actions server in background
rasa run actions &
# Start rasa server with nlu model
rasa run --enable-api --cors "*" --debug -p $PORT