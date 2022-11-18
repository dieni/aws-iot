# aws-iot

# Setup the Virtual Envionment
It is possible to setup a virtual Pyhton environment and installing all necessary components for the project useing Make:

```
make venv-setup
```

And to activate the environment
```
source .venv/bin/activate
```


# Run the client
in src/client/client.py configure
1. HOST to refer the endpoint of your aws iot server
2. Certificates for the thing that subscribes to the topic. Make sure that the thing has the correct permission by defining a policy for it!

Run the client
```
python3 src/client/client.py
```

# Run Thing to publish messages
in src/thing/thing.py configure
1. ENDPOINT to refer the endpoint of your aws iot server
2. Certificates for the thing that publishes to the topic. Make sure that the thing has the correct permission by defining a policy for it!

Run the publisher
```
python3 src/thing/thing.py
```

You should now be able to see the published messages printed by the client.