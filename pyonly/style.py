# This StyleObject class simulates the HTML DOM Style Object.
class StyleObject():
    def __init__(self, window, element, specialchars):
        self.window = window                                                # The Window object is required to communicate with JavaScript.
        self.element = element                                              # This property contains the JavaScript code to access the HTML element.
        self.specialchars = specialchars

    # The following __getattr__ and __setattr__ dunder/magic methods cover every property of the HTML DOM Style Object.
    async def __getattr__(self, name):
        return await self.window.get(self.element + ".style."+ name +";")

    def __setattr__(self, name, value):
        if name == "window" or name == "element" or name == "specialchars":                                 # These attributes should be added to the StyleObject object as properties:
            self.__dict__[name] = value
        else:                                                                                               # Otherwise, a value is assigned to the property of an HTML element using JavaScript code:
            self.window.execute(self.element + '.style.'+ name +' = "' + self.specialchars(value) + '";')
