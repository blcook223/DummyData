# DummyData

A Sublime Text plugin for generating dummy JSON data.

Turn this:

![screenshot of Sublime Text editor with open dummy data model file](/docs/images/model.png)

Into this:

![screenshot of Sublime Text editor with open dummy data results file](/docs/images/results.png)


## How to Use DummyData

### Installing DummyData

DummyData is available through [Package Control](https://packagecontrol.io/).

To install manually, execute the command `git clone https://github.com/blcook223/DummyData.git` in your Sublime Text `Packages` directory.

### Getting Started

To see how DummyData works, try the following:

1. Open a new file, and type the following:

        {
            "an integer": "{% integer 1 10 %}",
            "true or false": "{% boolean %}",
            "random selection": "{% random \"first string\" \"second string\" %}"
        }

2. Right click, and select "Generate DummyData".

3. View the results in the newly opened file.

DummyData works by interpreting a DummyData model, which is simply a JSON file that may contain function tags. Function tags are strings in the format `"{% function_name arg_1 arg_2 %}"`. When DummyData interprets a model, it produces a new JSON file, replacing tags with random, dummy JSON data.


### Generating Dummy JSON

DummyData adds two commands to Sublime Text:

- New DummyData Model

This command can be accessed via Tools > DummyData in the main menu or in the command palette under "DummyData: New Model". This opens a new JSON file containing a sample DummyData model, which can be modified, saved, and used to generate dummy JSON.

- Generate DummyData

This command becomes available when editing a JSON file. It can be accessed via Tools > DummyData in the main menu, in the command palette under "DummyData: Generate DummyData", or in the right-click menu under "Generate DummyData". This command parses the currently edited JSON file, including any function tags you have included, and produces a new file containing dummy JSON.


## DummyData Functions

### integer

`{% integer [min], [max] %}`

The `integer` function returns a random integer between the `min` and `max` values inclusive. If no arguments are provided, `integer` randomly returns either `0` or `1`.

### number

`{% number [min], [max], [decimals] %}`

The `number` function returns a random floating decimal point number between the `min` and `max` values inclusive. If no arguments are provided, `number` returns a random number between `0` and `1`. If `decimals` is specified, the function will return a number with the specified maximum number of digits after the decimal point.

### datetime

`{% datetime [format], [start], [end] %}`

The `datetime` function will return a random date and time in the given format between the specified start and end datetimes. If no arguments are supplied, `datetime` will return the current date and time. See [Python datetime documentation](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior) for details on date formatting. If no format is given, input and output dates must be in `'%m/%d/%Y %I:%M%p'` format.

### date

`{% date [format], [start], [end] %}`

The `date` function will return a random date in the given format between the specified start and end dates. If no arguments are supplied, `date` will return today's date. See [Python datetime documentation](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior) for details on date formatting. If no format is given, input and output dates must be in `'%m/%d/%Y'` format.

### time

`{% time [format], [start], [end] %}`

The `time` function will return a random time in the given format between the specified start and end times. If no arguments are supplied, `time` will return the current system time. See [Python datetime documentation](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior) for details on date formatting. If no format is given, input and output dates must be in `'%I:%M%p'` format.

For backwards compatibility, when no format is given, the `time` function supports hours without zero-padding.

### random

`{% random [arg1], [arg2], ... [argn] %}`

The `random` argument randomly selects from a set of provided arguments. There are two ways to use the `random` function:

* With arguments, e.g.:

`"{% random \"a string\" \"another string\" %}"`

If string arguments are supplied, `random` will randomly select from the arguments provided and return a string.

* Without arguments, e.g.:

`["{% random %}", "a string", 10, true, null, ["an", "array"], {"an": "object"}]`

If no arguments are supplied, the `{% random %}` tag must be the first element in an array. The `random` function will then choose randomly from among the JSON entities supplied in the rest of the list.

### repeat

`{% repeat [times] %}`

The `repeat` function generates an array of JSON entities following a specified structure. The `{% repeat %}` tag must be the first element in an array. For example, the `repeat` function could be used in a DummyData model as follows:

    [
        "{% repeat 6 %}",
        {
            "name": "{% first_name %} {% last_name %}"
        }
    ]

This model would produce something similar to the following:

    [
        {
            "name": "Terry Jones"
        },
        {
            "name": "Graham Chapman"
        },
        {
            "name": "Michael Palin"
        },
        {
            "name": "John Cleese"
        },
        {
            "name": "Eric Idle"
        },
        {
            "name": "Terry Gilliam"
        }
    ]

### index

`{% index %}`

The `index` function returns an integer indicating the iteration of a `repeat` function. The `index` function can only be used within a `repeat` structure (see above).

### boolean

`{% boolean %}`

The `boolean` function returns a random `true` or `false` value.

### postal

`{% postal %}`

The `postal` function returns a random five-digit postal code.

### phone

`{% phone %}`

The `phone` function returns a random ten-digit phone number in this format: `(XXX) XXX-XXXX`.

### paragraph

`{% paragraph %}`

The `paragraph` function returns a paragraph of "lorem ipsum" text.

### sentence

`{% sentence %}`

The `sentence` function returns a sentence of "lorem ipsum" text.

### city

`{% city %}`

The `city` function returns a random city name.

### state

`{% state %}`

The `state` function returns a random US state name.

### street

`{% street %}`

The `street` function returns a random street name.

### country

`{% country %}`

The `country` function returns a random country name.

### company

`{% company %}`

The `company` function returns a random, fictional company name.

### first_name

`{% first_name %}`

The `first_name` function returns a random first name.

### last_name

`{% last_name %}`

The `last_name` function returns a random last name.

### uid

`{% uid %}`

The `uid` function will return a random, unique string of characters.

### url

`{% url %}`

The `url` function will return a random, fictional URL.

### email

`{% email %}`

The `email` function will return a random, fictional email address.
