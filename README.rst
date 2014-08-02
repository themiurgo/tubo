Tubo
====

Tubo is a library that provides a simple pipeline system for Python.

Unix pipe system is an excellent example of the concept of **separation of responsibility**. Each utility does a single thing well. This increases readability, maintainability of code and code reuse. Tubo wants to bring this abstraction to Python.

Usage
-----

You have a source of iterable items and you want to perform various operations on them. In a Unix-like system you would write something like this:

.. code-block:: bash

    cat foo.txt | op1 | op2 | op3

Using Tubo, instead, you would use Python and you would write something like this:

.. code-block:: pycon

    >>> output = tubo.pipeline(file('foo.txt'), op1, op2, op3)

And the output would be available for you, to print it or to further transform it as you prefer. The advantage is that you can write the operations in Python, giving you a lot of flexibility.

Create a pipeline
-----------------

The central part of Tubo is the method `tubo.pipeline`. It accepts an arbitrary number of arguments, the first being a *data source* and the following being *operations* on iterable data, defined using python generators.

**Each operation should `yield` something, so that the following operation can work.**

Example: capitalize words that contain a `i` letter.

.. code-block:: python

    text = ['italy', 'germany', 'brazil', 'france', 'england',
        'argentina', 'peru', 'united states', 'australia',
        'sweden', 'china', 'poland', 'portugal']

    def capitalize(lines):
        for line in lines:
            for word in line.split(","):
                yield word.capitalize()

    def filter_wordwith_i(words):
        for word in words:
            if 'i' in word:
              yield word

    output = tubo.pipeline(
        text,
        filter_wordwith_i,
        capitalize,
    )

At this point, output is an iterable, and we can do anything we want with it. We can print it or further transform it.

Merge two or more iterables
---------------------------

Sometimes, you need to write functions that take two or more inputs, and process them. In this case, you need to write an operation that accepts a **list of iterables**.

Example: interleave lines from two or more files (such as the utility `paste`)

.. code-block:: python

    def interleave(listoflines):
        for lines in itertools.izip(*listoflines):
            yield ''.join(lines)

    output = tubo.pipeline(
        (file('file1.txt'), file('file2.txt')),
        interleave
    )

Consume iterators at C-speed
----------------------------

Once you have your pipeline, it's time to consume it.

.. code-block:: python

    tubo.consume(output)

    # Equivalent to:
    # 
    # for element in output:
    #     pass 

This consumes the iterator at C-speed, and uses `this recipe <https://docs.python.org/2/library/itertools.html#recipes>`_.


Examples
--------

Reverse text of unique lines, append the number of lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def uniq(lines):
        seen = set()
        for line in lines:
            if line not in seen:
                seen.add(line)
                yield line

    def reverse_string(lines):
        for line in lines:
            yield ''.join(reversed(line))

    def append_nlines(lines):
        for nlines, line in enumerate(lines):
            yield line
        yield "\nTotal Number of lines: {}".format(nlines+1)

    steps = [
        uniq,
        reverse_string,
        append_nlines,
    ]

    output = tubo.pipeline(
        open(filename),
        uniq,
        reverse_string,
        append_nlines,
        iterprint
    )

Concatenate two files 1st words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When we need to merge two inputs, or two results of different pipes, we will use the functions `merge` and `merge_longest`, which will 

.. code-block:: python

    def select_Nth_word(N, lines):
        for line in lines:
            yield line.split(' ')[N]
    select_first_word = functools.partial(select_Nth_word, 0)
    select_second_word = functools.partial(select_Nth_word, 1)

    def concatenate(words):
        for word1, word2 in words:
            yield "{} {}".format(word1, word2)

    pipeline1 = tubo.pipeline(
        open(fname1),
        select_first_word,
    )
    pipeline2 = tubo.pipeline(
        open(fname2),
        select_second_word,
    )
    output = tubo.pipeline(
        tubo.merge(
            pipeline1,
            pipeline2,
        ),
        concatenate
    )

Credits
-------

The library was inspired from a `post by Christoph Rauch <http://engineering.stylight.com/pipes-and-filters-architectures-with-python-generators/>`_.
