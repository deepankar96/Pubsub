def send_msg(routing_key):
  props = session.delivery_properties(routing_key=routing_key)
  for i in range(5):
     session.message_transfer(destination="amq.topic", message=Message(props,routing_key + " " + str(i)))

send_msg("Sikkim.news")

send_msg("Sikkim.weather")

send_msg("Delhi.news")

send_msg("Delhi.weather")

# Signal termination
props = session.delivery_properties(routing_key="control")
session.message_transfer(destination="amq.topic", message=Message(props,"That's all, folks!"))

