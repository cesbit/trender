Template Render Engine
======================

Why TRender?
------------
It's just another template render engine so why choose TRender?
TRender is created for SiriDB which needed a very *fast*, *memory leak free* and *simple* template engine.

- *Fast*: 
	TRender is able to render the SiriDB main page 1000x in 0.03 seconds.
- *No Memory Leaks*: 
	No circular references are created, this is important for some projects (like SiriDB) who 
	want to use Python with gc (garbage collection) disabled.
- *Simple*:
 	Well, you have to decide for yourself if this is a good thing. TRender is 
 	not very, very rich in it's capabilities but still can include and extend templates,
 	has conditional statements, for loops and can use blocks and macros. The template
 	language looks a bit like Quik (another template engine) but is somewhat different.
 	 
Quick usage
-----------
```python
from trender import TRender

template = '@greet world!'
compiled = TRender(template)
output = compiled.render({'greet': 'Hello'})

print(output) # => Hello world! 
```	
	
Basics
------
TRender can use both a simple string as input or a filename. 

When using a filename we also need to specify a path, like: `
```python
TRender('base.template', path='path_to_file')
```

Note that path should be the root path for your templates so assume we have the following path structure:

	/templates/
	/templates/pages/
			base.template
	/templates/components/
			component.template
			
Then it's best to initialize TRender like `TRender('pages/base.template', '/templates')` so the engine will be
able to find `components/component.template` when used inside your template.

Both `#extend` and `#include` are only available when using a template file, not with a simple string.

Using variable
--------------
Variable in a template are prefixed with an `@` and optionally can be closed with a `!` exclamation mark. A variable can only include alphabetic characters, digits and underscores. (And a `.`, but this has a special meaning to select nested variable). If you want a 'real' `@` in the template, add `!` as an escape character.

Examples:
```python
# Just render a simple variable...

TRender('@name is perfect').render({
	'name': 'Iris'
}) 
# Output => "Iris is perfect"
```

```python
# Escape @ to render an email address...
	
TRender('@name@!@domain').render({
	'name': 'iris', 
	'domain': 'home.nl'
})
# Output => "iris@home.nl"
```

```python
# Use nested variable (you can use nesting as deep as you want)...

TRender('@person.name is @person.age years old').render({
	'person': {
		'name': 'Iris', 
		'age': 2
	}
})
# Output => "Iris is 2 years old"
```

```python
# Close variable when needed...

TRender('@name!IsPerfect').render({
	'name': 'Iris'
})
# Output => "IrisIsPerfect"
```

Comments
--------
Comments should start with `##` or a `#` followed by a `space`.

Example:
```
# This is a comment line
##This is a comment line too
```

Conditionals
------------
Conditionals are very simple in TRender. We evaluate a simple value or allow a function for more complex conditionals.
We start with `#if` followed by an optional `#elif` finally an optional `else` and close with `#end`. 
If a conditional is not available in the namespace it will evaluate as `false`.

Simple example:
```python
TRender('''

#if @perfect:
	I'm perfect
#elif @almost_perfect:
	I'm almost perfect
#else:
	I'm not perfect..
#end

''').render({'almost_perfect': true}) 

# Output => "I'm almost perfect"
```

Complex example (actually it's not really complex...)
```python
TRender('''

#if @old_enough(@person.age):
	I'm old enough
#else:
	I'm NOT old enough
#end

''').render({
	'old_enough': lambda age: age >= 18,
	'person': {'age': 37}
})

# Output => "I'm old enough"
```

Loops
-----
We use `#for` loops and the loop should always close with `#end`.

Since an example explains more than words:
```python
TRender('''

#for @person in @people:
	@person.name is @person.age years old
#end

''').render({
	'people': [
		{'name': 'Iris', 'age': 2},
		{'name': 'Sasha', 'age': 30}
	]
})

# Output =>
#	Iris is 2 years old
#	Sasha is 30 years old
```

Blocks
------
Sometimes you want to define a block an re-use this block several times. As a name convention I like to write blocks using CamelCase.

Example:
```python
TRender('''

#block Item:
    <li>@item</li>
#end

<ul>
#for @item in @items.black:
    #Item
#end
</ul>

''').render({
    'items': ['laptop', 'mouse']
})

# Output =>
#    <ul>
#        <li>laptop</li>
#        <li>mouse</li>
#    </ul>
```

Macros
------
Macros are like blocks, except that they will be compiled only once using the namespace where the macro is defined. For example if we had used a `macro` in the `block` example above, we would get two empty `<li></li>` items since `@item` was not avaible when defining the macro. As a name convention I like to write blocks using UPPERCASE_CHARACTERS.

Include
-------
Including files is only possible when using a template file as source. Includes happen at compile time so they have no extra costs during rendering. 

Example:
```html
# base.template
<h1>Let include a file</h1>
#include another.template
<span>Yes, it worked!</span>
```
```html
# another.template
<span>Please, include me...</span>
```
```python
# Now compile and render the templates
TRender('base.template', '.').render()

# Output =>
#    <h1>Let include a file</h1>
#    <span>Please, include me...</span>
#    <span>Yes, it worked!</span>
```

Extend
------
Extend can be used to extend a template. This is ofter useful when we want to use a `base` template but start rendering another specific template. It's only possible to use extend when using a template file as source.

Example:
```html
# base.template
<html>
<head>
<title>I'm a base template</title>
</head>
<body>
#CONTENT
</body>
</html>
```
```html
# some.template
#extend base.template:

#macro CONTENT:
<span>This is just some content...</span>
#end <!-- End of CONTENT -->

#end <!-- End of extend base.template -->
```
```python
# Now compile and render the templates
TRender('some.template', '.').render()

# Output =>
#    <html>
#    <head>
#    <title>I'm a base template</title>
#    </head>
#    <body>
#    <span>This is just some content...</span>
#    </body>
#    </html>
```
		
How to use TRender with aiohttp (web server)
--------------------------------------------
TRender can used together with the `aiohttp` web server by using simple decorators for loading and rendering templates. 

Example:
```python
from trender.aiohttp_template import setup_template_loader
from trender.aiohttp_template import template

# This will setup the template loader. Make sure you run this only once.
setup_template_loader('/my_template_path')


# The 'template' decorator can be used to load a template.
# we assume in this example that you have the following template:
#
#   /my_template_path/base.template
#
# and you want to render this using the namespace:
#
#   {'name': 'Iris'}

@template('base.template')
async def myhandler(request):
	return {'name': 'Iris'}
	
# Thats it!
```
