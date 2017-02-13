import psycopg2 as pg
from interfaces import IStorage, IStorageAdapter, IAccountingEntry
from zope.interface import implementer
from zope.component import getGlobalSiteManager, adapter, getAdapter

@implementer(IStorage)
class PostgresStorage:
    def __init__(self, db=None,
        host=None,
        port=None,
        user=None,
        password=None):
        self.conn=pg.connect("""
            host={}
            port={}
            user={}
            password={}
            dbname={}
            """.format(host, port, user, password, db)
        )

    def store(self, obj):
        adapted_obj=getAdapter(obj, IStorageAdapter)
        adapted_obj.store_into(self)

@adapter(IAccountingEntry)
@implementer(IStorable)
class AccountingEntryToPostgresStorageAdapter:
    def __init__(self, obj):
        self.obj=obj

    def store_into(self, storage):
        o = self.obj
        conn = storage.conn
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO entries
                (cr, dr, amount, currency, moment)
            VALUES
                ("{}", "{}", "{}", {}, "{}");
            """.format(o.cr, o.dr,
                        o.amount, o.currency,
                        o.moment)
        )
        cur.commit()
        rc=cur.fetchone()
        print(rc)
        self.rc = rc

    def organize(self, storage):
        conn = storage.conn
        cur = conn.cursor()
        cur.execute("""
            CREATE SEQUENCE acc_entries;
            """)
        cur.commit();
        cur.execute("""
            CREATE TABLE entries  IF NOT EXISTS (
                id integer PRIMARY KEY DEFAULT nextval('acc_entries'),
                cr varchar(10),
                dr varchar(10),
                amount numeric(4),
                currency integer,
                moment timestamp
            )
        """)
        cur.commit()

storage=PostgresStorage(host='172.16.19.20',
    port=15432, user='acc', password='acc',
    db='acc'
    )

GSM=getGlobalSiteManager()
GSM.registerUtility(storage, name="acc")
GSM.registerAdapter(EntryToPostgresStorageAdapter)
