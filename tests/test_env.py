# coding: utf-8
import os
import pytest
import sys
from mock import patch
from decouple import ConfigEnv
from faults import ImproperlyConfigured

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO


ENVFILE = '''
KeyTrue=True
KeyOne=1
KeyYes=yes
KeyOn=on

KeyFalse=False
KeyZero=0
KeyNo=no
KeyOff=off

#CommentedKey=None
PercentNotEscaped=%%
NoInterpolation=%(KeyOff)s
'''


def test_env_comment():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        with pytest.raises(ImproperlyConfigured):
            config('CommentedKey')

def test_env_percent_not_escaped():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert '%%' == config('PercentNotEscaped')

def test_env_no_interpolation():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert '%(KeyOff)s' == config('NoInterpolation')

def test_env_bool_true():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert True == config('KeyTrue', cast=bool)
        assert True == config('KeyOne', cast=bool)
        assert True == config('KeyYes', cast=bool)
        assert True == config('KeyOn', cast=bool)

def test_env_bool_false():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert False == config('KeyFalse', cast=bool)
        assert False == config('KeyZero', cast=bool)
        assert False == config('KeyNo', cast=bool)
        assert False == config('KeyOff', cast=bool)

def test_env_os_environ():
    os.environ['KeyFallback'] = 'On'
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert True == config('KeyTrue', cast=bool)
        assert True == config('KeyFallback', cast=bool)
    del os.environ['KeyFallback']

def test_env_not_null():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        with pytest.raises(ImproperlyConfigured):
            config('KeyNotNull')

        assert True == config('KeyNotNull', default=True, cast=bool)

def test_env_not_null_with_default_none():
    with patch('decouple.open', return_value=StringIO(ENVFILE), create=True):
        config = ConfigEnv('.env')
        assert None == config('KeyNotNull', default=None, null=True)
