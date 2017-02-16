from isu.enterprise.configurator import createConfigurator
createConfigurator(ini='tests.ini', name='')

from isu.enterprise.components import *
from zope.component import getUtility, getAdapter
import isu.enterprise.sqlstorage
from nose.tools import nottest
from nose.plugins.skip import Skip
class IsuEnterpriseTests:
    def setUp(self):
        pass

    def test_something(self):
        assert 1 + 1 == 2

    def tearDown(self):
        pass


class TestEntryImplementation:
    def setUp(self):
        self.e = Entry("50", "71", 1000)

    def tearDown(self):
        pass

    def test_implementation(self):
        assert IAccountingEntry.implementedBy(Entry)

    def test_provision(self):
        assert IAccountingEntry.providedBy(self.e)

    def test_construction(self):
        assert self.e.cr == "50", "wrong credit account"
        assert self.e.currency == 643
        assert self.e.moment is not None

class TestStorage:
    def setUp(self):
        self.store = getUtility(IStorage, name="acc")

    def test_conn_good(self):
        assert self.store.conn is not None


class TestPostgesStorageAdapter(TestEntryImplementation):
    def setUp(self):
        TestEntryImplementation.setUp(self)
        TestStorage.setUp(self)

    def test_save(self):
        self.store.store(self.e)
