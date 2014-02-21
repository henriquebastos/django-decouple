# coding: utf-8
import pytest
import sys
from faults import ImproperlyConfigured
from mock import patch, mock_open
from decouple import ConfigIni

# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    from io import StringIO
else:
    from StringIO import StringIO



INIFILE = '''
[settings]
KeyTrue=True
KeyOne=1
KeyYes=yes
KeyOn=on

KeyFalse=False
KeyZero=0
KeyNo=no
KeyOff=off

#CommentedKey=None
PercentIsEscaped=%%
Interpolation=%(KeyOff)s
'''


def test_ini_comment():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        with pytest.raises(ImproperlyConfigured):
            config('CommentedKey')

def test_ini_percent_escape():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        assert '%' == config('PercentIsEscaped')

def test_ini_interpolation():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        assert 'off' == config('Interpolation')

def test_ini_bool_true():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        assert True == config('KeyTrue', cast=bool)
        assert True == config('KeyOne', cast=bool)
        assert True == config('KeyYes', cast=bool)
        assert True == config('KeyOn', cast=bool)

def test_ini_bool_false():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        assert False == config('KeyFalse', cast=bool)
        assert False == config('KeyZero', cast=bool)
        assert False == config('KeyNo', cast=bool)
        assert False == config('KeyOff', cast=bool)

def test_env_not_null():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        with pytest.raises(ImproperlyConfigured):
            config('KeyNotNull')

        assert True == config('KeyNotNull', default=True, cast=bool)

def test_env_not_null_with_default_none():
    with patch('decouple.open', return_value=StringIO(INIFILE), create=True):
        config = ConfigIni('settings.ini')
        assert None == config('KeyNotNull', default=None, null=True)
