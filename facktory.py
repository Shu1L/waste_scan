# coding=utf-8

import sys
import traceback

def factory(moduleName, **args):
    try:
        __import__(moduleName)
    except Exception as e:
        raise Exception('Error Import Plugin: ' + moduleName + '， Exception: ' + str(e))
    else:
        className = moduleName.split('.')[-1]

        try:
            aModule = sys.modules[moduleName]
            aClass = getattr(aModule, className)
        except:
            raise Exception('Error Load Plugin: ' + moduleName + '.')
        else:
            try:
                inst = aClass(*args)
            except Exception as e:
                msg = 'Error Instance: ' + className + ', Exception: ' + str(e) + ', Traceback: ' + str(
                    traceback.format_exc())
                raise Exception(msg)
            return inst

