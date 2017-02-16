import psycopg2
from isu.enterprise.interfaces import IStorage, IStorable
from isu.enterprise.interfaces import IAccountingEntry, IConfigurator
from zope.interface import implementer
from zope.component import getGlobalSiteManager, adapter, getAdapter, getUtility


@implementer(IStorage)
class PostgresStorage:

    def __init__(self, db=None,
                 host=None,
                 port=None,
                 user=None,
                 password=None):
        self.conn = psycopg2.connect("""
            host={}
            port={}
            user={}
            password={}
            dbname={}
            """.format(host, port, user, password, db)
        )

    def store(self, obj):
        adapted_obj = getAdapter(obj, IStorable)
        adapted_obj.store_into(self)


@adapter(IAccountingEntry)
@implementer(IStorable)
class AccountingEntryToPostgresStorageAdapter:

    def __init__(self, obj):
        self.obj = obj

    def store_into(self, storage):
        o = self.obj
        conn = storage.conn
        tries = 2
        while tries > 0:
            try:
                cur = conn.cursor()
                CMD = \
                    """
                    INSERT INTO acc_entries
                        (cr, dr, amount, currency, moment)
                    VALUES
                        (%s, %s, %s, %s, %s)
                    RETURNING id;
                """
                cur.execute(CMD, (o.cr,
                                  o.dr,
                                  o.amount,
                                  o.currency,
                                  o.moment))
                _id = cur.fetchone()[0]
                conn.commit()
                # print(_id)
                self.rc = _id
                cur.close()
                return o
            except psycopg2.ProgrammingError as E:
                print(E, "\n", CMD)
                conn.rollback()
                cur.close()
                self.organize(storage)
                tries -= 1
                print("retry", tries)

        raise RuntimeError("cannot save object")

    def organize(self, storage):
        conn = storage.conn
        cur = conn.cursor()
        cur.execute("""
            CREATE SEQUENCE IF NOT EXISTS acc_entries_sequence;
            """)
        conn.commit()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS acc_entries (
                id integer PRIMARY KEY DEFAULT nextval('acc_entries_sequence'),
                cr varchar(10),
                dr varchar(10),
                amount numeric(4),
                currency integer,
                moment timestamp
            );
        """)
        conn.commit()
        cur.close()

conf = getUtility(IConfigurator)
database = conf.get("storage","key").strip()
if database=="postgres":
    pconf = conf["postgres"]
    storage = PostgresStorage(\
        host=pconf.get("host", fallback="127.0.0.1").strip(),
        port=pconf.getint("port", fallback="5432"),
        user=pconf.get("user", fallback="acc").strip(),
        password=pconf.get("password", fallback="acc"),
        db=pconf.get("db", fallback="acc")
    )

    GSM = getGlobalSiteManager()
    GSM.registerUtility(storage, name="acc")
    GSM.registerAdapter(AccountingEntryToPostgresStorageAdapter)
