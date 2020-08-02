from pyonly import element

class HTMLCollection:
    def __init__(self, window, identifier):
        self.window = window

        # This property contains the JavaScript code to access the HTMLCollection.
        self.identifier = identifier
    
    # This method is used to update the len property of the HTMLCollection object with the value of the length property of the DOM HTMLCollection.
    async def update(self):
        self.len = int(await self.window.get(self.identifier + ".length;"))

    # This method returns the HTML element at the given index/name/ID in an HTMLCollection as HTML_Element object.
    def __getitem__(self, index):
        # If a string is passed, the HTML element at the specified ID or name in an HTMLCollection is returned.
        if type(index) == str:
            return element.HTML_Element(self.window, self.identifier + '["' + index + '"]')
        
        # Otherwise, the HTML element at the specified index in an HTMLCollection is returned.
        elif index < self.len and (index * -1) <= self.len:
            if index < 0:
                index = self.len + index
            return element.HTML_Element(self.window, self.identifier + "[" + str(index) + "]")
        else:
            raise StopIteration
    
    def __setitem__(self, index, value):
        self.window.execute(self.identifier+ "[" + str(index) + "] = " + str(value))
    
    # This magic method returns the len property that should equal the number of the contained HTML elements.
    def __len__(self):
        return self.len
    
    # This method returns the HTML element at the specified index in an HTMLCollection as HTML_Element object.
    def item(self, index):
        return element.HTML_Element(self.window, self.identifier + "[" + str(index) + "]")
    
    # This method returns the HTML element at the specified ID or name in an HTMLCollection as HTML_Element object.
    def namedItem(self, name):
        return element.HTML_Element(self.window, self.identifier + '["' + name + '"]')
    
    # This method updates the len property of the HTMLCollection object with the value of the length property of the DOM HTMLCollection.
    # Additionally, this value is returned.
    @property
    async def length(self):
        self.len = int(await self.window.get(self.identifier + ".length;"))
        return self.len
