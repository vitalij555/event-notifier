![Upload Python Package](https://github.com/vitalij555/event-notifier/workflows/Upload%20Python%20Package/badge.svg)

# event-notifier

Simple python notifier.

## Contents

- [Background](#background)
- [Installation](#installation)
- [Usage](#usage)
- [Constructor](#constructor)
- [Available Functions](#available-functions)
- [Tests](#tests)
- [License](#license)
- [Contributing](#contributing)

## Background

This is the 

## Installation

```
pip install event-notifier
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
addEventSubscriber(eventName, subscriber)
```

**Parameters**

- `url` - `string` - optional, Events API URL, default: `http://localhost:4000`
- `space` - `string` - optional, space name, default: `default`
- `configurationUrl` - `string` - optional, Configuration API URL. By default, it's the same as `url` but with `4001` port
- `connectorUrl` - `string` - optional, Connector API URL. By default, it's the same as `url` but with `4002` port
- `accessKey` - `string` - optional, access key for hosted Event Gateway. Access key is required for using Configuration API methods on hosted Event Gateway

**Example**

```python
import Notifier

notifier = Notifier(["onCreate", "onOpen", "onModify", "onDelete"])

```

## Available Functions

```python
addEventSubscriber(eventName, subscriber)
```

### some Function Name here

TBD

**Example**

```python
#TBD
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
