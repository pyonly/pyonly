from pyonly import style


# This class includes all methods/(properties) related to an HTML element.
class HTML_Element:
    def __init__(self, window, element, deleteReference_command=None):
        self.objectProperties = ["window", "element", "deleteReference_command", "style", "eventHandlers"]  # This property contains all the names of the attributes
                                                                                                            # that are to be assigned to the HTML_Object as a property in the __setattr__ method.
        self.window = window                                                                                # The Window object is required to communicate with JavaScript.
        self.element = element                                                                              # This property contains the JavaScript code to access the HTML element.
        self.deleteReference_command = deleteReference_command                                              # This property is needed in case an HTML element is created. 
                                                                                                            # It contains the JavaScript code to delete the respective property 
                                                                                                            # of the Python.Created_Elements_references object so that the 
                                                                                                            # HTML element can no longer be accessed.
        
        self.style = style.StyleObject(self.window, self.element, self.specialchars)                        # This object simulates the HTML DOM Style Object

        # The following property contains the names of all DOM onevents. 
        # This enables the __setattr__ method to determine from the name that an onevent handler should be added to the respective HTML element.
        self.eventHandlers = ["onabort", "onafterprint", "onbeforeprint", "onbeforeunload", "onblur", "oncanplay", "oncanplaythrough", "onchange", "onclick", "oncontextmenu", "oncopy", "oncut", "ondblclick", "ondrag", "ondragend", "ondragenter", "ondragleave", "ondragover", "ondragstart", "ondrop", "ondurationchange", "onended", "onerror", "onfocus", "onfocusin", "onfocusout", "onfullscreenchange", "onfullscreenerror", "onhashchange", "oninput", "oninvalid", "onkeydown", "onkeypress", "onkeyup", "onload", "onloadeddata", "onloadedmetadata", "onloadstart", "onmessage", "onmousedown", "onmouseenter", "onmouseleave", "onmousemove", "onmouseover", "onmouseout", "onmouseup", "onoffline", "ononline", "onopen", "onpagehide", "onpageshow", "onpaste", "onpause", "onplay", "onplaying", "onpopstate", "onprogress", "onratechange", "onresize", "onreset", "onscroll", "onsearch", "onseeked", "onseeking", "onselect", "onshow", "onstalled", "onstorage", "onsubmit", "onsuspend", "ontimeupdate", "ontoggle", "ontouchcancel", "ontouchend", "ontouchmove", "ontouchstart", "onunload", "onvolumechange", "onwaiting", "onwheel"]
    
    # The following __getattr__ and __setattr__ dunder/magic methods cover every property of the HTML Element.
    async def __getattr__(self, name):
        return await self.window.get(self.element + "."+ name +";")
    
    def __setattr__(self, name, value):
        if name == "objectProperties":  # This attribute should be added to the HTML_Element object as property:
            self.__dict__[name] = value
        elif name in self.objectProperties: # These attributes should be added to the HTML_Element object as properties:
            self.__dict__[name] = value
        elif name in self.eventHandlers: # If the name is the same as the name of a DOM event, an event handler should be added to the respective HTML element:

            # The value parameter of this __setattr__ method must contain the name of the Python function to be executed when the event occurs.
            # When the assigned event occurs, the Python.call method is called in the JavaScript code. 
            # The name of the Python function to be called is passed to this method together with the arguments received from the event. 
            # The received argument is mostly an event object. So that this event object can be converted into a JSON string, all circular references must be removed, 
            # which is what the processArguments and processEventObject methods do.
            self.window.execute(self.element + '.' + name + ' = function() { Python.call.apply(null, ["' + self.specialchars(value) + '"].concat(Python.processArguments(arguments))); };')
            
        else:   # Otherwise, a value is assigned to the property of an HTML element by using JavaScript code:
            self.window.execute(self.element + '.' + name + ' = "' + self.specialchars(value) + '";')


    # This method changes the attribute value of an HTML element.
    def setAttribute(self, attr, val):
        self.window.execute(self.element + '.setAttribute("' + self.specialchars(attr) + '", "' + self.specialchars(val) +  '");')



    def addEventListener(self, eventType, func_name, useCapture = "false"):
        self.window.execute(self.element + '.addEventListener("' + self.specialchars(eventType) + '", function() { Python.call.apply(null, ["' + self.specialchars(func_name) + '"].concat(Python.processArguments(arguments))); }, "' + self.specialchars(useCapture) +  '");')
    

    # The HTML element is added to the body.
    def append_this_to_body(self):
        self.window.execute('document.body.appendChild(' + self.element + ');')
    

    # In case an HTML element has been created, JavaScript code is passed during the initialization of the HTML_Element object
    # allowing to delete the respective property of the Python.Created_Elements_references object
    # so that the HTML element can no longer be accessed.
    def deleteReference(self):
        if self.deleteReference_command != None:
            self.window.execute(self.deleteReference_command)
    
    def specialchars(self, s):
        s = s.replace("\\", "\\\\")
        return s.replace('"', '\\"')

