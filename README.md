# The perfect Chatbot
### A Rasa Application

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

### Creating pipelines for your model

* The first component in the pipeline is usually a tokenizer, which breaks up the user input into individual tokens. In this example, we are using the WhitespaceTokenizer, which simply splits the input on whitespace.

* The next components in the pipeline are feature extractors, which convert the input tokens into feature vectors that can be used by the machine learning models. In this example, we are using the RegexFeaturizer and CountVectorsFeaturizer, which create bag-of-words representations of the input.

* The next components are the entity extractors, which identify and extract entities from the input text. In this example, we are using the CRFEntityExtractor and EntityExtractor components, which use conditional random fields and lookup tables, respectively, to extract entities.

* The EntitySynonymMapper component maps different entity values to a single canonical value. For example, "NYC" and "New York City" might be mapped to the same entity value.

* The Embedding component learns distributed representations of words in the input text. These embeddings are used as input to the DIETClassifier, which is a neural network-based classifier that predicts the intent and entities in the input.

* The final component in the pipeline is the ResponseSelector, which selects the appropriate response to the user input from a predefined set of responses.


You can choose to create a minimal pipeline, with just a Tokeniser, Featuriser and Intent Classifier and Entity Extractor

The current pipeline used in this project
```
pipeline:
  - name: WhitespaceTokenizer
  - name: LanguageModelFeaturizer
    model_name: "bert"
    model_weights: "rasa/LaBSE"
  - name: DIETClassifier
    epochs: 200
```

* WhitespaceTokenizer: Splits words into whitespace
* LanguageModelFeaturizer: Creates vector representation using model specified
* DIETClassifier: A Featurizer combines intent classification and entity recognition into a single model that uses a neural network to extract features from the input text


For more deatils checkout RASA's official blogs on all available options for Featurizers, Tokenizers, Intent Classifiers, Entity Extractors
https://rasa.com/docs/rasa/2.x/components/#languagemodelfeaturizer 