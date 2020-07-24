import tornado
import json

from pyonly import document

# It contains all WebSocket connections.
clients = []

# It contains all app objects related to the WebSocket connections.
clientapps = []

# This function returns a WebSocketHandler-object.
def Handler(App):
    class WebSocketHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True

    # Invoked when a new WebSocket is opened
        def open(self):
            if self not in clients:
                clients.append(self)        # A WebSocket is appended to the clients list.
                newapp = App(Window(self))  # A new app object is created for a new WebSocket. 
                                            # Furthermore, a Window-object containing the Websocket is passed as an argument to the __init__() function of the app object.
                                            # IMPORTANT: In the init function, this passed Window-object must be assigned to the object property with the name window ("self.window")
                                            # so that this attribute can be accessed in the on_message method.
                clientapps.append(newapp)   # This new object is added to the clientapps list.

    # Handle incoming messages on the WebSocket
        async def on_message(self, message):
            for i in range(0, len(clients)):
                if self == clients[i]:                                                                                              # The index of the WebSocket in the clients and clientapps lists is determined.
                    arguments = json.loads(message)                                                                                 # The JSON string is parsed to a Python dictionary 
                                                                                                                                    # to get the send data/arguments from JavaScript.
                                                                                                                                    # The key "target" defines the purpose of the call/what should be done.
                    if arguments["target"] == "callfunc":                                                                           # If the value of the key "target" is "callfunc", 
                                                                                                                                    # Python invokes the method of the key "funcname" 
                                                                                                                                    # together with the arguments defined by the key "args". 
                        try:
                            func_to_call = getattr(clientapps[i], arguments["func_name"])
                            clientapps[i].window.getEvent_listener = tornado.ioloop.asyncio.Event()
                            clientapps[i].window.getWaiter = tornado.ioloop.asyncio.create_task(func_to_call(*arguments["args"]))
                        except AttributeError:
                            print("Error calling the method (without callback): " + arguments["func_name"])
                    
                    elif arguments["target"] == "callfunc_async":                                                                   # If the value of the key "target" equals "callfunc_async", 
                                                                                                                                    # Python invokes the method of the key "funcname"
                                                                                                                                    # together with the arguments defined by the key "args"
                                                                                                                                    # (similarly to the case when "target" is "callfunc").
                                                                                                                                    # Subsequently, a return value is expected, 
                                                                                                                                    # which is sent back to the JavaScript function by using the callback method.
                        try:
                            func_to_call = getattr(clientapps[i], arguments["func_name"])
                            clientapps[i].window.getEvent_listener = tornado.ioloop.asyncio.Event()
                            async_func_to_call = tornado.ioloop.asyncio.create_task(func_to_call(*arguments["args"]))
                            func_result = await async_func_to_call
                            clientapps[i].window.callback(func_result)
                            #print(func_result.result())
                        except AttributeError:
                            print("Error calling the method: " + arguments["func_name"])
                    elif arguments["target"] == "get":                                                                              # If the value of the key "target" equals "get", Python calls
                                                                                                                                    # the return_get_value method of the Window object
                                                                                                                                    # to set and clear the "getEvent_listener" (Event) 
                                                                                                                                    # and to return the value to the waiting get method of the Window-object.
                        await clientapps[i].window.return_get_value(arguments["args"])
        
        # Invoked when the WebSocket is closed.
        def on_close(self):
            for i in range(0, len(clients)):
                if self == clients[i]:          # The index of the WebSocket in the clients and clientapps lists is determined to remove the items.
                    del clients[i]
                    del clientapps[i]
                    break
    
    return WebSocketHandler

# It handels the communication between Python  and JavaScript.
# Furthermore it simulates the JavaScript window object in Python.
class Window:
    def __init__(self, websocket):
        self.websocket = websocket                      # WebSocketHandler
        self.retValue = ""                              # It handles the return value in case the get method is called.
        self.getWaiter = None
        self.getEvent_listener = None                   # This contains an asyncio Event object to enable the get method waiting for the send value from JavaScript (case: "target" == "get") to return it.
        self.document = document.Document(self)         # This Document object simulates the HTML DOM document object.
    
    def execute(self, code):                            # This method exists to execute JS-Code. Compared to the get method no value is returned. 
        arguments = {                                   # The variable "arguments" is a dictionary containing the key "task" with the value "execute" to transmit the JavaScript onMessage method what to do.
            "task": "execute",
            "code": code                                # The value of the key "code" contains the JavaScript code to be executed.
        }
        json_args = json.dumps(arguments)               # Finally, the dictionary is converted into a JSON string to send it to JavaScript.
        self.websocket.write_message(json_args)
    
    def callback(self, result):                         # This method calls JavaScript awaiting a return value of an executed Python function. 
        arguments = {                                   # The dictionary "arguments" contains the key "task" with the value "callback" to transmit JavaScript the purpose/what to do. 
            "task": "callback",
            "code": result                              # The value of the key "code" is the return value of an executed Python function for that JavaScript is awaiting.
        }
        json_args = json.dumps(arguments)               # Finally, the dictionary is converted into a JSON string to send it to JavaScript.
        self.websocket.write_message(json_args)
    
    async def get(self, code, givenargs=None):          # This method is invoked to execute JavaScript code and to get the returned value.
        arguments = {
            "task": "get",                              # The dictionary "arguments" contains the key "task" with the value "get" to transmit JavaScript the purpose/what to do.
            "code": code                                # The value associated with the key "code" is the JavaScript code to be executed.
        }
        if givenargs != None:                           # In case a return value is also expected, but another dictionary should be sent 
            arguments = givenargs                       # to JavaScript in the form of a converted JSON string, there is this option of overwriting the dictionary "arguments".
        
        json_args = json.dumps(arguments)               # The dictionary is converted into a JSON string to send it to JavaScript.
        self.retValue = ""
        self.websocket.write_message(json_args)
        
        await self.getEvent_listener.wait()             # It waits until the getEvent_listener is set.
                                                        # This Event object is set when the return_get_value method is called.
        return self.retValue

    async def return_get_value(self, value):            # This method is called when a value from JavaScript should be returned.
        self.retValue = value                           # This value is assigned to the retValue property.
        self.getEvent_listener.set()                    # Finally, the getEvent_listener can be set so that in the get method the retValue can be returned.
        self.getEvent_listener.clear()
        #await self.getWaiter
    
    async def call(self, func_name,*argtuple):          # This method is invoked when a JavaScript function should be called.
        arguments = {                                   # The dictionary "arguments" has got the key "task" with the value "call" to determine JavaScript to call a specific function.
            "task": "call",
            "func_name": func_name,                     # The value of the key "func_name" is the name of the JavaScript function to be invoked.
            "args": argtuple,                           # The value associated with the key "args" contains the arguments to be passed to the JS function.
        }
        return await self.get("undefined", arguments)   # The value of the get method is awaited to return it.
                                                        # The get method expects at least one argument, namely the JavaScript code to be executed.
                                                        # Since a structure to wait for a JavaScript result is required, the get method can be used with some changes.
                                                        # Instead of executing JavaScript code, a function should be called. 
                                                        # Consequently, the dictionary "arguments" must be overwritten.
                                                        # Therefore the parameter "givenargs" exists. 
        

