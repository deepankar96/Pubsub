def dump_queue(queue):

  content = ""		             # Content of the last message read
  final = "That's all, folks!"   # In a message body, signals the last message
  message = 0

  while content != final:
    try:
      message = queue.get(timeout=10)
      content = message.body
      session.message_accept(RangedSet(message.id)) 
      print content
    except Empty:
      print "No more messages!"
      return


def subscribe_queue(server_queue_name, local_queue_name):

  print "Subscribing local queue '" + local_queue_name + "' to " + server_queue_name + "'"

  queue = session.incoming(local_queue_name)

  session.message_subscribe(queue=server_queue_name, destination=local_queue_name)
  queue.start()

  return queue


# declare queues on the server

news = "news-" + session.name
weather = "weather-" + session.name
Sikkim = "Sikkim-" + session.name
Delhi = "Delhi-" + session.name

session.queue_declare(queue=news, exclusive=True)
session.queue_declare(queue=weather, exclusive=True)
session.queue_declare(queue=Sikkim, exclusive=True)
session.queue_declare(queue=Delhi, exclusive=True)



session.exchange_bind(exchange="amq.topic", queue=news, binding_key="#.news")
session.exchange_bind(exchange="amq.topic", queue=weather, binding_key="#.weather")
session.exchange_bind(exchange="amq.topic", queue=Sikkim, binding_key="Sikkim.#")
session.exchange_bind(exchange="amq.topic", queue=Delhi, binding_key="Delhi.#")

# Bind each queue to the 'control' binding key so we know when to stop

session.exchange_bind(exchange="amq.topic", queue=news, binding_key="control")
session.exchange_bind(exchange="amq.topic", queue=weather, binding_key="control")
session.exchange_bind(exchange="amq.topic", queue=Sikkim, binding_key="control")
session.exchange_bind(exchange="amq.topic", queue=Delhi, binding_key="control")

# Subscribe local queues to server queues

local_news = "local_news"
local_weather = "local_weather"
local_Sikkim = "local_Sikkim" 
local_Delhi = "local_Delhi"

local_news_queue = subscribe_queue(news, local_news)
local_weather_queue = subscribe_queue(weather, local_weather)
local_Sikkim_queue = subscribe_queue(Sikkim, local_Sikkim)
local_Delhi_queue = subscribe_queue(Delhi, local_Delhi)

# Call dump_queue to print messages from each queue

print "Messages on 'news' queue:"
dump_queue(local_news_queue)

print "Messages on 'weather' queue:"
#dump_queue(local_weather_queue)

print "Messages on 'Sikkim' queue:"
dump_queue(local_Sikkim_queue)

print "Messages on 'Delhi' queue:"
dump_queue(local_Delhi_queue)

