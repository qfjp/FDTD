"""
.. module:: tags.tags
   :platform: Unix, Windows
   :synopsis: Extra annotations for python class-level methods

.. moduleauthor:: Daniel Pade <djpade@gmail.com>
"""
import warnings


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def new_func(*args, **kwargs):
        """
        deprecated tag message
        """
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func
