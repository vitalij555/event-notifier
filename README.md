![Upload Python Package](https://github.com/vitalij555/event-notifier/workflows/Upload%20Python%20Package/badge.svg)

# event-notifier

Simple python notifier.

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Constructor](#constructor)
 updated- [API Overview](#api-overview)
- [Tests](#tests)
- [License](#license)
- [Contributing](#contributing)

## Background

This is the 

## Installation

```
pip install -U event-notifier
```

## Usage


```python
import Notifier
```

TBD
Example taken from the internet showing how to mark it down inside .md file:
The `emit()` function takes three arguments: 
- an `event` which is a valid CloudEvent,
- a `path` which is the path associated to the function (default: `/`)
- a `headers` object that represents the headers sent to the gateway (default: `{"Content-type": "application/json"}`)

The function returns a request object. If your event has a `sync` subscription attached, the `fetch` response will have the status code and body from the subscription. If not, the response will return a `202 Accepted` status code with an empty body.

## Constructor

```python
Notifier(eventNames, logger=None)
```

**Parameters**

- `eventNames` - `list` - mandatory, provides list of all supported events. Values provided here later can be used for raising events  
- `logger` - `object` - optional, space name, default: `None`


## API Overview

```python
fireEvent(self, eventName, *args, **kwargs)
```
```python
removeSubscribersByEventName(self, eventName)
```
```python
removeAllSubscribers(self)
```

```python
addEventSubscriber(self, eventName, subscriber)
```

```python
addEventSubscriber(eventName, subscriber)
```

**Parameters**

- `url` - `string` - optional, Events API URL, default: `http://localhost:4000`
- `space` - `string` - optional, space name, default: `default`
- `configurationUrl` - `string` - optional, Configuration API URL. By default, it's the same as `url` but with `4001` port
- `connectorUrl` - `string` - optional, Connector API URL. By default, it's the same as `url` but with `4002` port
- `accessKey` - `string` - optional, access key for hosted Event Gateway. Access key is required for using Configuration API methods on hosted Event Gateway



### some Function Name here


**Example**

```python
from EventNotifier import Notifier


class FileWatchDog():
	def onOpen(self, fileName, openMode):
		print(f"File {fileName} opened with {openMode} mode")
		
			
	def onClose(self, fileName):
		print(f"File {fileName} closed")
	

watchDog = FileWatchDog()	
	
	
notifier = Notifier(["onCreate", "onOpen", "onModify", "onClose", "onDelete"])

notifier.addEventSubscriber("onOpen",  watchDog.onOpen)
notifier.addEventSubscriber("onClose", watchDog.onClose)

notifier.fireEvent("onOpen", openMode="w+", fileName="test_file.txt")  # order of named parameters is not important
notifier.fireEvent("onClose", fileName="test_file.txt")
```
Will produce:
```console
$ python test.py
File test_file.txt opened with w+ mode
File test_file.txt closed
```

### some other Function Name here

Utility to print the current configuration.

**Example**

```python
#TBD
```

## Tests

[PyTest][pytest] is used for tests. Python 2 is not supported.

**Install PyTest**

```sh
$ pip install pytest
```

**Run tests**

```sh
$ py.test test/*
```

[pytest]: http://pytest.org/


## License

License
Copyright (C) 2020 Vitalij Gotovskij

event-notifier binaries and source code can be used according to the MIT License


## Contribute
TBD
