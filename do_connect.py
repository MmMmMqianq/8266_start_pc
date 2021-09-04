def do_connect():
  import network
  import time
  
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('MMMMMMMMM', 'qsq19931219')
    while not wlan.isconnected():
      pass
  print('connect successful,network ifconfig:', wlan.ifconfig())
  ip = wlan.ifconfig()
  return ip
