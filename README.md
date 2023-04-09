# The perfect Chatbot

To start the chatbot using the command line
```
rasa shell
```

To test the NLU components
```
rasa shell nlu
```

If you're going to use stories which has asociated actions, don't forget to start the server
```
rasa run actions
```

To test if all your YAML files are in correct format you can:
```
rasa data validate
```

To test sample stories are corret:
```
rasa test
```

## Supported Stories
This chatbot currently supports the following stories:

* Report COVID status and ask about test type
* Find student ID

## Have to test if pipeline is working
* Add Test Stories to tests/test_stories.yml
* Test using ```rasa data validate```
