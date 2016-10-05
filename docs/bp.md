# Python

We follow the [PEP8 style guide for Python](http://www.python.org/dev/peps/pep-0008/).  Docstrings follow [PEP257](http://www.python.org/dev/peps/pep-0257/). The rest of the document describes additions and clarifications to the PEP documents that we follow at Khan Academy.

You can use `make lint` from the top level of the website source tree to run a pep8 check over all the source code or `make linc` to check only files you've changed. You should aim to not introduce any new violations, before checking in code.

## Indentation

Use 4 spaces -- never tabs -- for indentation.

This is a strict rule and ignoring this can (has) cause(d) bugs.

## \_\_init\_\_.py

Unless an exception is explicitly allowed by a codebase owner (Kamens or Jason, for now), `__init__.py` files should be empty.

> *Rationale:* when you do `import foo.bar` python imports two files: `foo/bar.py`, and `foo/__init__.py`. If `foo/__init__.py` has imports of its own, those will be run as well -- even if you don’t plan to run any of the code defined in `__init__.py`. This slows down execution, and worse causes circular-import problems that could be entirely avoided.

If you have code that you think every user of every function inside this directory needs to run first, `__init__.py` may be appropriate, but you should also consider just creating a function that executes that code, and running the function at the top level (that is, not indented) inside each file in your directory. This makes it more obvious what's going on, and also makes it easier to special-case certain files if the need ever arises.

Using `__init__.py` to bring variables from sub-modules into the main module space totally defeats the point of having sub-modules in the first place; don’t do it.

For more discussion, see http://stackoverflow.com/questions/1944569/how-do-i-write-good-correct-init-py-files.

## Imports

### from...import

Only import entire modules, never individual symbols from a module. For top-level modules, that means `import foo`. For sub-modules, you can do either `import foo.bar` or `from foo import bar`.
```py
import auth_util                      # module import: importing the file auth_util.py
import auth.oauth_credentials         # module import: importing the file auth/oauth_credentials.py
from auth import oauth_credentials    # module import: importing the file auth/oauth_credentials.py
from auth_util import get_response    # BAD: symbol import: importing the function get_response from auth_util.py
from auth_util import Authorize       # BAD: symbol import: importing the class Authorize from auth_util.py
from auth_util import AUTH_HOST       # BAD: symbol import: importing the variable AUTH_HOST from auth_util.py
```
*Exception:* for third-party code, where the module documentation explicitly says to import individual symbols.

If the basename of a sub-module is generic, prefer the import form to the from form, otherwise either is fine:

```py
import auth.models                   # code uses auth.models.Token -- clear

from auth import models              # code uses models.Token -- ambiguous!

from auth import oauth_credentials   # code uses oauth_credentials.Token -- clear
```

> Rationale: This is the single best -- and easiest -- way to avoid the circular-import problem. To simplify, when you say `import x`, Python executes the `x.py` file, but doesn't need to get any attributes from it.  When you say `from x import foo`, Python needs `x.py` to be executed enough that `foo` is defined in it.  When `x` does a 'from-import' from `y`, and `y` does a 'from-import' from `x`, the circular import can succeed if a partial module is enough (as it will be with `import x`), but it can fail if the circularity happens before the needed attribute is defined (as it might be with `from x import foo`).

> *Side note:* While this rule helps with most circular-import problems, it doesn’t help with all: a module `x` may still need symbols from a module `y` while `x` is still being imported. For instance, if you say `class xclass(y.yclass): ...`, Python needs the `yclass` attribute at import-time.

The downside of this rule is that code gets more verbose: where before you could do

```py
from possibly_a_very_long_name import MyClass
[...]
m = MyClass(...)
```

now you have to do

```py
import possibly_a_very_long_name
[...]
m = possibly_a_very_long_name.MyClass(...)
```

I argue, though, this verbiage is beneficial: in the same way that self.xxx is an immediate sign at the point of use that xxx is a member of the current class, x.MyClass is an immediate sign that MyClass comes from file x (which often tells you more about what MyClass is for, and makes it easier to find in the source as well). This often tells you enough that you can continue reading the code, without needing a context switch to look up the where MyClass is defined and what it says.

## Import style

All imports should be at the top of the file, separated (by blank lines) into three sections: system imports, third-party imports (including appengine), and khan academy-written imports. All non-system imports should be specified relative to the root of the ka python tree; do not use absolute_import. Each section should be sorted alphabetically. Only one import should be on each line.

> *Rationale:* When I see autocomplete.foo() in the code, and I want to know what it does, it’s helpful to know if I should be looking on the web (because autocomplete is part of the python distribution), or in the local source tree (because autocomplete is written by us). It’s also helpful to know if it’s code we wrote (and the barrier to hacking on it is low) or code someone else wrote (which means it may be easier to just work around any problems I have with it). The three sections tell me that with just a quick glance at the top of the file. Plus, since each section is alphabetical, it’s easy for me to find the import within the section.

Alphabetical sorting is by the main module name (so second word of the line), and ignores case:

```py
import api
from app import App
from app import Zebra
import auth_models
import NonExistentModule
[...]
```

Here are some constructs that are not consistent with this style rule:
```py
from app import App, Zebra    # BAD: two imports on the same line
import .models                # BAD: relative import.  Alternative: from <curmodule> import models
```

We are planning (as of 13 April 2012) on moving to a world where third-party (aka ‘vendor’) code all lives in a third_party/ directory, making this rule easier to follow. Until then,don't get too worked up about whether oauth_provider imports (say) are in section 2 or section 3.

## Docstrings

All non-trivial methods should have docstrings. Docstrings should follow guidelines here: [PEP257](http://www.python.org/dev/peps/pep-0257/).  For more examples, see the [Google style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments) around docstrings.

To summarize: There are two types of docstrings, long-form and short-form.

A short-form docstring fits entirely on one line, including the triple quotes. It is used for simple functions, especially (though by no means exclusively) ones that are not part of a public API:

```py
"""Return a user-readable form of a Frobnozz, html-escaped."""
```

Note that the text is specified as an action (“return”) rather than a description (“returns”). This has the added advantage of taking less space, so the comment is more likely to fit on a single line. :-)

If the description spills past one line, you should move to the long-form docstring: a summary line (one physical line) starting with a triple-quote ("""), terminated by a period, question mark, or exclamation point, followed by a blank line, followed by the rest of the doc string starting at the same cursor position as the first quote of the first line, ending with triple-quotes on a line by themselves. (Unlike what the BDFL suggests in PEP 257, we do not put a blank line before the ending quotes.)

```py
"""This comment serves to demonstrate the format of a docstring.

Note that the summary line is always at most one line long, and
on the same line as the opening triple-quote, and with no spaces
between the triple-quote and the text.  Always use double-quotes
(") rather than single-quotes (') for your docstring.   (This
lets us reserve ''' (3 single-quotes) as a way of commenting out
big blocks of code.
"""
```

A function (including methods and generators) must have a docstring, unless it meets all of the following criteria:

- not externally visible
- very short
- obvious

The docstring should describe the function's calling syntax and its semantics, not its implementation.

The docstring should end with the following special sections (see [the Google style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments) for more details).

- **Arguments:** List each parameter by name, and a description of it. The description can span several lines (use a hanging indent if so). Use instead of "Args". 
- **Returns:** (or **Yields:** for generators): Describe the type and semantics of the return value. If the function only returns None, this section is not required.
- **Raises:** List all exceptions that are relevant to the interface.

Classes should follow a similar format: a single line describing the class, plus more details, but instead of Arguments/Returns/Raises, it should have an Attributes: section that lists and describes the public attributes of the class (if any).

Modules (files) should have a docstring too, at the top of the file, starting with the usual one-line summary:  
```py
"""One line summary.

Longer description.
"""
```

> Rationale: People will read a piece of code many more times than they will write it. Time spent documenting at write-time more than pays off at read time. What is obvious to you as the code-author, well versed in the module where this function lives, may not be at all obvious to a code reader, who is possibly jumping into this function from some unrelated part of the codebase.

The rules here may seem like overkill, especially the need to document every argument and return value. I can say from experience two things: it often does seem like overkill when writing it (especially when the docstring is longer than the function!) but I've almost never thought it was overkill when reading unfamiliar code. You may find, as you write the docstring, you're putting down something that wasn't as obvious as you thought it was:

```py
def WriteTimestamp(now):
    """Write the current time to stdout in an arbitrary user-readable format.

    Arguments:
        now: the current time as a time_t. Should be time.time() except for tests.
    """
    ...
```

Even though the meaning of now may seem obvious, it's not obvious that it's only being passed in so it can be mocked out for tests. Its type also isn't obvious (a time_t? a tuple? a datetime object?), so it's nice to have that documented as well.

## Top of the file

Start your file with a module docstring. Do not put a shebang line (`#!/usr/bin/python`) or copyright notice, or anything else.  Follow the docstring with your imports; don't put an `__author__` line.

> *Exception:* if the python file is meant to be executable, it should start with the following shebang line:

> ```py
#!/usr/bin/env python
```

> *Rationale:* a shebang line is useless for non-executable files. An `__author__` line just gets out of date, and is better determined by looking at source control history in any case. Code is automatically copyrighted; a copyright line doesn't help. No need to put this useless boilerplate at the top of the file!

TODO(csilvers): should we put in a line indicating licensing?

## Unused variables

If you want to assign a value to a variable that will not be used again, name the variable either `_` (python convention) or `unused_<something>` (less-well-known python convention).  This will keep our lint checkers from complaining.

## Splitting lines

Using PEP8 as a guideline for Python formatting runs us head-long into a great debate: the 79-character line limit. For better or worse, the PEP8 limit is part of the lint check for Khan Academy's Python code.

> Rationale: short lines have benefits, including:

> - Broad tool support. Code is read more frequently than it is written, often by those whose tools don't match the original author. Short lines are always well-supported. Many tools only naively support long lines (`<pre>` tags and most terminal tools), and no editor wraps long lines intelligently enough in all cases.
> - Side-by-side code windows. Try it out, it's great.
> - A free gut check. It's easy to reach 100 or 200 columns when writing complex expressions or nesting deeply. If this indicates unclear code, future readers would appreciate a quick refactoring.

> Of course having a hard limit for line length is silly. Any reasonable limit runs into a case where breaking the rule produces better code. However, having unnecessarily long lines scattered about due to assumptions about a reader's tools is also silly.

Python expressions end with a newline, not a semicolon, unlike many C-based languages. The trick is that lines can be continued within parentheses, brackets, and braces, or following a backslash. Parentheses are recommended. Backslashes should be avoided.

```py
>>> True and (True or
...           False)


>>> [x * x
...  for x
...  in xrange(0, 10)
...  if x % 2]


>>> {'Earth': 1,
...  'Jupiter': 5.3,
...  'Saturn': 9}
```

Notably, splitting string literals doesn't require use of the + operator. Adjacent literals are automatically combined.

```py
>>> twist = 'Peter Piper ' 'split a set ' 'of simple strings'
>>> twist
'Peter Piper split a set of simple strings'
```

This makes splitting long messages easy.

```py
>>> twist = ('Peter Piper '
...          'split a set '
...          'of simple strings')
```

Because Python's indentation style is unlike many C-based languages, your editor might need some cajoling to support it.

- Emacs has great support out of the box via `python-mode`.
- Vim needs some help. Installing [this indent script by Eric Mc Sween](http://www.vim.org/scripts/script.php?script_id=974) will get you there.

Examples of line splitting from our code:

```py
BAD:  zero_duration_videos = video_models.Video.all().filter("duration =", 0).fetch(10000)

GOOD: zero_duration_videos = (video_models.Video.all()
                        .filter("duration =", 0)
                        .fetch(10000))
```

```py
# BAD:
return current_app.response_class("OAuth error. %s" % e.message, status=401, headers=build_authenticate_header(realm="http://www.khanacademy.org"))

# GOOD:
return current_app.response_class(
    "OAuth error. %s" % e.message, status=401,
    headers=build_authenticate_header(realm="http://www.khanacademy.org"))
```

```py
# Bad:
kwargs = dict((str(key), value) for key, value in topic_json.iteritems() if key in ['id', 'title', 'standalone_title', 'description', 'tags', 'hide'])
# Good:
kwargs = dict((str(key), value)
              for key, value in topic_json.iteritems()
              if key in ['id', 'title', 'standalone_title',
                         'description', 'tags', 'hide'])
```

## Splitting tricky lines

There are cases where line splitting doesn't feel nice. Let's look at a few of them, sigh, and move on.

This long method reference needs surrounding parens and splits the line before the dot operator:

```py
# Bad:
badge_name = badges.topic_exercise_badges.TopicExerciseBadge.name_for_topic_key_name(self.key().name())
# Good:
badge_name = (badges.topic_exercise_badges.TopicExerciseBadge
              .name_for_topic_key_name(self.key().name()))
```

This long string path needs to be split.

```py
# Bad:
self.redirect("/class_profile?selected_graph_type=%s&coach_email=%s&graph_query_params=%s" %
        (self.GRAPH_TYPE, urllib.quote(coach.email), urllib.quote(urllib.quote(self.request.query_string))))
# Good:
self.redirect(
    "/class_profile?selected_graph_type=%s&coach_email=%s"
    "&graph_query_params=%s" % (
        self.GRAPH_TYPE,
        urllib.quote(coach.email),
        urllib.quote(urllib.quote(self.request.query_string))))
```

Sometimes, the best way to avoid long lines is to use temporary variables.  This can improve readability in any case.

```py
# Bad:
topics_list = [t for t in topics if not (
    (t.standalone_title == "California Standards Test: Algebra I" and t.id != "algebra-i") or
    (t.standalone_title == "California Standards Test: Geometry" and t.id != "geometry-2"))
    ]
# Good:
bad_title_and_ids = [("California Standards Test: Algebra I", "algebra-i"),
                     ("California Standards Test: Geometry", "geometry-2"),
                    ]
topics_list = [t for t in topics
               if not (t.standalone_title, t.id) in bad_title_and_ids]
```

## Indenting continued lines properly

When a logical statement is split into multiple lines and is followed by an indented line, the continued lines should be indented further to set them apart from the next logical statement.

In the following example taken from http://www.python.org/dev/peps/pep-0008/#maximum-line-length, notice how the second and third lines of the if condition are indented further to differentiate them from the actual raise statement within the if block:

```py
class Rectangle(Blob):
    def __init__(self, width, height,
                     color='black', emphasis=None, highlight=0):
        if (width == 0 and height == 0 and
                color == 'red' and emphasis == 'strong' or
                highlight > 100):
            raise ValueError("sorry, you lose")
```

# The Best of the Best Practices (BOBP) Guide for Python

A "Best of the Best Practices" (BOBP) guide to developing in Python.

## In General

### Values

- "Build tools for others that you want to be built for you." - Kenneth Reitz
- "Simplicity is alway better than functionality." - Pieter Hintjens
- "Fit the 90% use-case. Ignore the nay sayers." - Kenneth Reitz
- "Beautiful is better than ugly." - [PEP 20][]
- Build for open source (even for closed source projects).

### General Development Guidelines

- "Explicit is better than implicit" - [PEP 20][]
- "Readability counts." - [PEP 20][]
- "Anybody can fix anything." - [Khan Academy Development Docs][]
- Fix each [broken window](http://www.artima.com/intv/fixit2.html) (bad design, wrong decision, or poor code) *as soon as it is discovered*.
- "Now is better than never." - [PEP 20][]
- Test ruthlessly. Write docs for new features.
- Even more important that Test-Driven Development--*Human-Driven Development*
- These guidelines may--and probably will--change.

## In Particular

### Style

Follow [PEP 8][], when sensible.

#### Naming

- Variables, functions, methods, packages, modules
    - `lower_case_with_underscores`
- Classes and Exceptions
    - `CapWords`
- Protected methods and internal functions
    - `_single_leading_underscore(self, ...)`
- Private methods
    - `__double_leading_underscore(self, ...)`
- Constants
    - `ALL_CAPS_WITH_UNDERSCORES`

###### General Naming Guidelines 

Avoid one-letter variables (esp. `l`, `O`, `I`). 

*Exception*: In very short blocks, when the meaning is clearly visible from the immediate context

**Fine**
```python
for e in elements:
    e.mutate()
```

Avoid redundant labeling.

**Yes**
```python
import audio

core = audio.Core()
controller = audio.Controller()
```

**No**
```python
import audio

core = audio.AudioCore()
controller = audio.AudioController()
```

Prefer "reverse notation".

**Yes**
```python
elements = ...
elements_active = ...
elements_defunct = ...
```

**No**
```python
elements = ...
active_elements = ...
defunct_elements ...
```

Avoid getter and setter methods.

**Yes**
```python
person.age = 42
```

**No**
```python
person.set_age(42)
```

#### Indentation

Use 4 spaces--never tabs. Enough said.

#### Imports

Import entire modules instead of individual symbols within a module. For example, for a top-level module `canteen` that has a file `canteen/sessions.py`,

**Yes**

```python
import canteen
import canteen.sessions
from canteen import sessions
```

**No**

```python
from canteen import get_user  # Symbol from canteen/__init__.py
from canteen.sessions import get_session  # Symbol from canteen/sessions.py
```

*Exception*: For third-party code where documentation explicitly says to import individual symbols.

*Rationale*: Avoids circular imports. See [here](https://sites.google.com/a/khanacademy.org/forge/for-developers/styleguide/python#TOC-Imports).

Put all imports at the top of the page with three sections, each separated by a blank line, in this order:

1. System imports
2. Third-party imports
3. Local source tree imports

*Rationale*: Makes it clear where each module is coming from.

#### Documentation

Follow [PEP 257][]'s docstring guidelines. [reStructured Text](http://docutils.sourceforge.net/docs/user/rst/quickref.html) and [Sphinx](http://sphinx-doc.org/) can help to enforce these standards.

Use one-line docstrings for obvious functions.

```python
"""Return the pathname of ``foo``."""
```

Multiline docstrings should include

- Summary line
- Use case, if appropriate
- Args
- Return type and semantics, unless ``None`` is returned

```python
"""Train a model to classify Foos and Bars.

Usage::

    >>> import klassify
    >>> data = [("green", "foo"), ("orange", "bar")]
    >>> classifier = klassify.train(data)

:param train_data: A list of tuples of the form ``(color, label)``.
:rtype: A :class:`Classifier <Classifier>`
"""
```

Notes

- Use action words ("Return") rather than descriptions ("Returns").
- Document `__init__` methods in the docstring for the class.

```python
class Person(object):
    """A simple representation of a human being.

    :param name: A string, the person's name.
    :param age: An int, the person's age.
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

##### On comments

Use them sparingly. Prefer code readability to writing a lot of comments. Often, small methods are more effective than comments.

*No*

```python
# If the sign is a stop sign
if sign.color == 'red' and sign.sides == 8:
    stop()
```

*Yes*

```python
def is_stop_sign(sign):
    return sign.color == 'red' and sign.sides == 8

if is_stop_sign(sign):
    stop()
```

When you do write comments, remember: "Strunk and White apply." - [PEP 8][]

#### Line lengths

Don't stress over it. 80-100 characters is fine.

Use parentheses for line continuations.

```python
wiki = (
    "The Colt Python is a .357 Magnum caliber revolver formerly manufactured "
    "by Colt's Manufacturing Company of Hartford, Connecticut. It is sometimes "
    'referred to as a "Combat Magnum". It was first introduced in 1955, the '
    "same year as Smith & Wesson's M29 .44 Magnum."
)
```

### Testing

Strive for 100% code coverage, but don't get obsess over the coverage score.

#### General testing guidelines

- Use long, descriptive names. This often obviates the need for doctrings in test methods.
- Tests should be isolated. Don't interact with a real database or network. Use a separate test database that gets torn down or use mock objects.
- Prefer [factories](https://github.com/rbarrois/factory_boy) to fixtures.
- Never let incomplete tests pass, else you run the risk of forgetting about them. Instead, add a placeholder like `assert False, "TODO: finish me"`.

#### Unit Tests

- Focus on one tiny bit of functionality.
- Should be fast, but a slow test is better than no test.
- It often makes sense to have one testcase class for a single class or model.

```python
import unittest
import factories

class PersonTest(unittest.TestCase):
    def setUp(self):
        self.person = factories.PersonFactory()

    def test_has_age_in_dog_years(self):
        self.assertEqual(self.person.dog_years, self.person.age / 7)
```

#### Functional Tests

Functional tests are higher level tests that are closer to how an end-user would interact with your application. They are typically used for web and GUI applications.

- Write tests as scenarios. Testcase and test method names should read like a scenario description.
- Use comments to write out stories, *before writing the test code*.

```python
import unittest

class TestAUser(unittest.TestCase):

    def test_can_write_a_blog_post(self):
        # Goes to the her dashboard
        ...
        # Clicks "New Post"
        ...
        # Fills out the post form
        ...
        # Clicks "Submit"
        ...
        # Can see the new post
        ...
```

Notice how the testcase and test method read together like "Test A User can write a blog post".


## Inspired by...

- [PEP 20 (The Zen of Python)][PEP 20]
- [PEP 8 (Style Guide for Python)][PEP 8]
- [The Hitchiker's Guide to Python][python-guide]
- [Khan Academy Development Docs][]
- [Python Best Practice Patterns][]
- [Pythonic Sensibilities][]
- [The Pragmatic Programmer][]
- and many other bits and bytes

[Pythonic Sensibilities]: http://www.nilunder.com/blog/2013/08/03/pythonic-sensibilities/
[Python Best Practice Patterns]: http://youtu.be/GZNUfkVIHAY
[python-guide]: http://docs.python-guide.org/en/latest/
[PEP 20]: http://www.python.org/dev/peps/pep-0020/
[PEP 257]: http://www.python.org/dev/peps/pep-0257/
[PEP 8]: http://www.python.org/dev/peps/pep-0008/
[Khan Academy Development Docs]: https://sites.google.com/a/khanacademy.org/forge/for-developers
[The Pragmatic Programmer]: http://www.amazon.com/The-Pragmatic-Programmer-Journeyman-Master/dp/020161622X/ref=sr_1_1?ie=UTF8&qid=1381886835&sr=8-1&keywords=pragmatic+programmer