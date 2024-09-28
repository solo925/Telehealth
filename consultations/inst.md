<!-- this cause problems -->

daphne -u /tmp/daphne.sock Telehealth.asgi:application

<!-- so use  -->

daphne -b 127.0.0.1 -p 8001 Telehealth.asgi:application
after that you have to change the websocket configuration to use the 8001 port as in

    chatSocket = new WebSocket(
      "ws://" + window.location.hostname + ":8001/ws/chat/" + roomName + "/"
    );

    it finnaly worked channels and daphne chat feature

video one device trial.one person working maybe i dont know moetesting needed
![alt text](image.png)
