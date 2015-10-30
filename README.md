Template Render Engine
----------------------

Why TRender?
============

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
===========


```python
from trender import TRender

template = '@greet world!'
compiled = TRender(template)
output = compiled.render({'greet': 'Hello'})

print(output) # => Hello world! 
```	
	
Basics
======

TRender can use both a simple string as input or a filename. When using a filename we also need to
specify a path, like: `TRender('base.template', path='path_to_file')`
 
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
==============

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

Conditionals
============

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
=====

We use `#for` loops and the loop should always close with `#end`.

Since an example explains more than words:

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
		Iris is 2 years old
		Sasha is 30 years old
	
		
Usage TRender with aiohttp (web server)
=======================================

TRender can used together with the `aiohttp` web server by using simple decorators for loading and rendering templates. 

Example:

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
	
