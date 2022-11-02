![Upload Python Package](https://github.com/vitalij555/event-notifier/workflows/Upload%20Python%20Package/badge.svg)
[![PyPi version](https://img.shields.io/pypi/v/event-notifier.svg?style=flat-square) ](https://pypi.python.org/pypi/event-notifier) [![Supported Python versions](https://img.shields.io/pypi/pyversions/event-notifier.svg?style=flat-square) ](https://pypi.org/project/event-notifier) [![License](https://img.shields.io/pypi/l/event-notifier.svg?style=flat-square) ](https://choosealicense.com/licenses) [![Downloads](https://pepy.tech/badge/event-notifier)](https://pepy.tech/project/event-notifier) [![codecov](https://codecov.io/gh/vitalij555/event-notifier/branch/master/graph/badge.svg)](https://codecov.io/gh/vitalij555/event-notifier)

# event-notifier

Library providing event registration and routing infrastructure.

## Contents

- [Background](#background)
- [Installation](#installation)
- [Example](#example)
- [Constructor](#constructor)
- [API Overview](#api-overview)
- [Tests](#tests)
- [License](#license)
- [Contributing](#contribute)


## Background

This is an implementation of event notifier (also known as emitter or dispatcher) allowing to notify one or more subscribers of an event that just occurred.

Any python object inheriting from or containing a notifier can act as event sender and any callable object can act as event receiver.
Allows to register receivers having variable number of arguments. 


## Installation

```
pip install -U event-notifier
```


## Example

```python
from EventNotifier import Notifier

# Imagine we have a piece of code which is interested in some events 
# occurring in other pieces of the code...
class FileWatchDog():
	def onOpen(self, fileName, openMode):
		print(f"File {fileName} opened with {openMode} mode")
		
			
	def onClose(self, fileName):
		print(f"File {fileName} closed")
	

watchDog = FileWatchDog()	
	
# Create Notifier object by providing a list of events other components might be interesting in	
notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

# From now other objects are able to subscribe to events we've declared above
# Its important to use the same name as it was declared while creating Notifier object
# Consider using constant declarations or enums in order to avoid typos here
notifier.subscribe("onOpen",  watchDog.onOpen)
notifier.subscribe("onClose", watchDog.onClose)

notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")  # order of named parameters is not important
notifier.raise_event("onClose", fileName="test_file.txt")
```
Will produce:
```console
$ python test.py
File test_file.txt opened with w+ mode
File test_file.txt closed
```


## Constructor

```python
Notifier(eventNames: list, logger=None)
```


**Parameters**

- `eventNames` - `list of any` - mandatory, provides list of all supported events. Values provided here can be used for raising events later.
 Values provided in this list can be of any type.
- `logger` - `object` - optional, logger supporting standard logging methods (info, warning error, etc..), default: `None`. 
If None is provided, then internal logger outputting warnings and errors to console will be created.



**Example**

Any object can be used as event name. Example below illustrates that:

```python
from EventNotifier import Notifier

class Box:
    def __init__(self, name):
        self.name = name

a = Box("name_BoxA")
b = Box("name_BoxB")


notifier = Notifier(["onCreate", 5, 22.58, "onDelete", a, b])

notifier.subscribe("onCreate", onCreateCallback)
notifier.subscribe(5, on5Callback)
notifier.subscribe(22.58, onFloatCallback)
notifier.subscribe(a, onBoxACallback)
notifier.subscribe(b, onBoxBCallback)


notifier.raise_event(5, "event: ! 5 !")  # on5Callback will be called with "event: ! 5 !" as parameter
notifier.raise_event(22.58, "event: ! 22.58 !")    # onFloatCallback will be called with "event: ! 22.58 !" as parameter
notifier.raise_event(b, "event: Box b")   # onBoxBCallback will be called with "event: Box b" as parameter
```


## API Overview


### subscribe(eventName, subscriber) 

**Description**

Adds callable subscribers interested in some particular event. 

**Parameters**

- `eventName` - `any` - mandatory, specifies name of the event, subscriber will be interested in.
- `subscriber` - `any` - mandatory, callable subscriber (function, class method or class with __call__ implemented)

**Example**

```python
from EventNotifier import Notifier

class CallableFileWatchdog:
	def __init__(self, pathToWatch):
		self.pathToWatch = pathToWatch
		

	def __call__(self, *args, **kwargs):
		if len(args) > 0:
			print(f"Event {args[0]} at path {self.pathToWatch} is called with following simple args: {[*args]} and with following keyword args: { {**kwargs} }")


callableWatchdog = CallableFileWatchdog("some\path\here")

notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])


notifier.subscribe("onCreate", callableWatchdog)
notifier.subscribe("onOpen",   callableWatchdog)


notifier.raise_event("onCreate", "onCreate", fileName="test_file.txt")
notifier.raise_event("onOpen", "onOpen", openMode="w+", fileName="test_file.txt") 
```
gives:
```console
Event onCreate at path some\path\here is called with following simple args: ['onCreate'] and with following keyword args: {'fileName': 'test_file.txt'}
Event onOpen at path some\path\here is called with following simple args: ['onOpen'] and with following keyword args: {'openMode': 'w+', 'fileName': 'test_file.txt'}
```


### subscribe_to_all(subscriber):

**Description**

Method allows to register one callable for all events supported by notifier.


**Parameters**

- `subscriber` - `callable` - mandatory, will be called when event rises.

**Example**

```python
from EventNotifier import Notifier
class CallableFileWatchdog:
    def __init__(self, pathToWatch):
	self.pathToWatch = pathToWatch


    def __call__(self, *args, **kwargs):
	if len(args) > 0:
	    print \
		(f"Event {args[0]} at path {self.pathToWatch} is called with following simple args: {[*args]} and with following keyword args: { {**kwargs} }")

callable_watchog = CallableFileWatchdog("some\\path\\here")
notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

notifier.subscribe_to_all(callable_watchog)

notifier.raise_event("onCreate", "onCreate", fileName="test_file.txt")
notifier.raise_event("onOpen", "onOpen", openMode="w+", fileName="test_file.txt")
```

Console output:

```console
Event onCreate at path some\path\here is called with following simple args: ['onCreate'] and with following keyword args: {'fileName': 'test_file.txt'}
Event onOpen at path some\path\here is called with following simple args: ['onOpen'] and with following keyword args: {'openMode': 'w+', 'fileName': 'test_file.txt'}
```


### get_registered_events():

**Description**

Returns all supported events as a list.

**Example**

```python
from EventNotifier import Notifier
notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])
print(notifier.get_registered_events())
```
will output:
```console
['onCreate', 'onOpen', 'onModify', 'onClose', 'onDelete']
```


### raise_event(eventName, *args, **kwargs)

**Description**

Rises specific event registered during initialization.

**Parameters**

- `eventName` - `any` - mandatory, name of the event to be raised.
- `*args` - `list` - optional, all simple parameters we want to pass to our subscribers (param1, param2, param3...).
- `**kwargs` - `dictionary` - optional, all named parameters we want to pass (param1=value1, param2=value2, param3=value3) 

**Example**

Check subscribe method's example link [above](#subscribeeventname-subscriber).


### remove_subscribers_by_event_name(event_name)

**Description**

Removes all subscribers for the specified event_name

**Parameters**

- `eventName` - `any` - mandatory, name of the event we want to remove subscribers for.

**Example**

```python
from EventNotifier import Notifier
class FileWatchDog():
    def onOpen(self, fileName, openMode):
        print(f"File {fileName} opened with {openMode} mode")

    def onClose(self, fileName):
        print(f"File {fileName} closed")


def onOpenStandaloneMethod(fileName, openMode):
    print(f"StandaloneMethod: File {fileName} opened with {openMode} mode")

watchDog = FileWatchDog()

notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

notifier.subscribe("onOpen", watchDog.onOpen)
notifier.subscribe("onOpen", onOpenStandaloneMethod)
notifier.subscribe("onClose", watchDog.onClose)

print("\nAfter subscription:")
notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")  # order of named parameters is not important
notifier.raise_event("onClose", fileName="test_file.txt")

notifier.remove_subscribers_by_event_name("onOpen")

print("\nAfter removal of onOpen subscribers:")
notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")  # order of named parameters is not important
notifier.raise_event("onClose", fileName="test_file.txt")

notifier.remove_subscribers_by_event_name("onClose")

print("\nAfter removal of onClose subscribers:")
notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")  # order of named parameters is not important
notifier.raise_event("onClose", fileName="test_file.txt")
```

will output:
```console
After subscription:
File test_file.txt opened with w+ mode
StandaloneMethod: File test_file.txt opened with w+ mode
File test_file.txt closed

After removal of onOpen subscribers:
File test_file.txt closed

After removal of onClose subscribers:
```


### remove_all_subscribers()

**Description**

Removes all subscribers for all events

**Example**

```python
from EventNotifier import Notifier
class FileWatchDog():
    def onOpen(self, fileName, openMode):
        print(f"File {fileName} opened with {openMode} mode")

    def onClose(self, fileName):
        print(f"File {fileName} closed")


def onOpenStandaloneMethod(fileName, openMode):
    print(f"StandaloneMethod: File {fileName} opened with {openMode} mode")

watchDog = FileWatchDog()

notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

notifier.subscribe("onOpen", watchDog.onOpen)
notifier.subscribe("onOpen", onOpenStandaloneMethod)
notifier.subscribe("onClose", watchDog.onClose)

print("\nAfter subscription:")
notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
notifier.raise_event("onClose", fileName="test_file.txt")

notifier.remove_all_subscribers()

print("\nAfter removal of all subscribers:")
notifier.raise_event("onOpen", openMode="w+", fileName="test_file.txt")
notifier.raise_event("onClose", fileName="test_file.txt")
```

will give:
```console
After subscription:
File test_file.txt opened with w+ mode
StandaloneMethod: File test_file.txt opened with w+ mode
File test_file.txt closed

After removal of all subscribers:
```



## Tests

[PyTest][pytest] is used for tests. Python 2 is not supported.

**Install PyTest**

```sh
$ pip install pytest
```

**Run tests**

```sh
$ pytest test/*
```

[pytest]: http://pytest.org/

**Check test coverage**

In order to generate test coverage report install pytest-cov:

```sh
$ pip install pytest-cov
```

Then inside test subdirectory call: 

```sh
pytest --cov=../EventNotifier --cov-report=html
```

## License

License
Copyright (C) 2020 Vitalij Gotovskij

event-notifier binaries and source code can be used according to the MIT License


## Contribute
TBD
