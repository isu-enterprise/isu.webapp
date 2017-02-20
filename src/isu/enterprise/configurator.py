from isu.enterprise.interfaces import IConfigurator
from zope.component import getGlobalSiteManager
import sys
if sys.version_info.major>2:
    from configparser import ConfigParser, ExtendedInterpolation
else:
    from ConfigParser import ConfigParser #, ExtendedInterpolation
import os

def registerConfigurator(obj, registry=None, name=""):
    if registry is None:
        registry=getGlobalSiteManager()
    registry.registerUtility(obj,
        provided=IConfigurator,
        name=name)

def createConfigurator(ini, registry=None, name=""):
    conf = ConfigParser(defaults=os.environ #,
        #interpolation=ExtendedInterpolation()
        )
    conf.read(ini)
    registerConfigurator(conf, registry=registry, name=name)

def initZCML():
    package=__name__
    xmlconfig(resource_stream(package, "configure.zcml"))


