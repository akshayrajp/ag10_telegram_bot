import sys
from query import Query as query
sys.path.append(".")


class Response:

    def help_text(self):
        return """
1. Radiation

2. Temperature

3. Humidity

4. All

Type the option number to proceed (Ex: 1)
"""

    def interact(self, user_messsage):

        # define emojis as variables using unicode strings
        wave = "\U0001F44B"

        # check input and produce appropriate response
        if(user_messsage == "hi" or user_messsage == "hello"):
            return "Hello there! " + wave
        elif(user_messsage == "bye" or user_messsage == "goodbye"):
            return "See you later! " + wave
        elif(user_messsage == "what's up" or user_messsage == "sup"):
            return "I\'m monitoring those sensors! How about you?"

    def undefined(self):
        # produce an appropriate response for undefined messages/behaviour
        response_text = "I don't understand. Please refer to the following help message:\n"
        response_text += self.help_text()
        return response_text

    def query_handler(self, input):

        # instantiate an object from class Query as 'Q'
        Q = query()

        # convert string to integer for ease of handling
        input = int(input)

        # check input and call appropriate methods
        climate_variables = ["usvh", "temp", "humid", "all"]
        return Q.preprocessor(climate_variables[input - 1])


def responses(input_text):

    # create object of class Response
    response = Response()

    # convert user input to lower-case for ease of processing
    user_messsage = str(input_text).lower()

    # check for casual interaction
    if user_messsage in (
        "hi", "hello",
        "bye", "goodbye",
            "what's up", "sup"):
        return response.interact(user_messsage)

    # check for help
    if user_messsage in ("help", "help?", "help!", "help."):
        return response.help_text()

    # perform operations based on numeric inputs (mostly running queries on InfluxDB)
    if int(user_messsage) in range(1, 10):
        return response.query_handler(user_messsage)

    # undefined user input response
    return response.undefined()
