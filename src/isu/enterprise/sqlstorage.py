import psycopg2
from isu.enterprise.interfaces import IStorage, IStorable
from isu.enterprise.interfaces import IAccountingEntry, IConfigurator
from zope.interface import implementer
from zope.component import getGlobalSiteManager, adapter, getAdapter, getUtility
import zope.interface

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

    def load(self, klass, id):
        gsm = getGlobalSiteManager()
        adapter_registry = gsm.adapters
        ifaces = list(zope.interface.implementedBy(klass))
        adapter = adapter_registry.lookup( \
            ifaces,
            IStorable)(obj=None)
        return adapter.load_from(self, id=id, klass=klass)

@adapter(IAccountingEntry)
@implementer(IStorable)
class AccountingEntryToPostgresStorageAdapter:

    def __init__(self, obj=None):
        if obj is not None:
            self.obj = obj
            if hasattr(obj, "__sql_id__"):
                self.id=obj.__sql_id__
            else:
                self.id=None

    def store_into(self, storage):
        o = self.obj
        conn = storage.conn
        if self.id is None:
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
                    cur.close()
                    # print(_id)
                    self.id = _id
                    o.__sql_id__=self.id
                    return o
                except psycopg2.ProgrammingError as E:
                    print(E, "\n", CMD)
                    conn.rollback()
                    cur.close()
                    self.organize(storage)
                    tries -= 1
                    print("retry", tries)
        else: # if self.id is not None
            cur = conn.cursor()
            CMD = \
                """
                UPDATE acc_entries AS e
                SET
                    (cr, dr, amount, currency, moment)
                =
                    (%s, %s, %s, %s, %s)
                WHERE e.id=%s;
            """
            cur.execute(CMD, (o.cr,
                            o.dr,
                            o.amount,
                            o.currency,
                            o.moment,
                            self.id))
            conn.commit()
            return o

        raise RuntimeError("cannot save object")

    def load_from(self, storage, klass, id):
        conn=storage.conn
        cur = conn.cursor()
        CMD = \
        """
        SELECT
            cr, dr, amount, currency, moment
        FROM
            acc_entries AS e
        WHERE
            e.id=%s
        """
        cur.execute(CMD, (id,))
        (cr,
            dr,
            amount,
            currency,
            moment) = cur.fetchone()
        o=self.obj = klass(cr=cr,dr=dr,
            amount=amount,
            currency=currency,
            moment=moment
            )
        self.id=id
        o.__sql_id__=id
        return o

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

# imidoev@mail.ru
