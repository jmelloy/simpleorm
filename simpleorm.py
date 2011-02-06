from datetime import datetime

class Query():
    def __init__(self, sql):
        self.sql = sql
    
    def __str__(self):
        return self.sql

    def exec_select(self, conn, return_type ='dict'):
        self.start_time = datetime.now()
        curs = conn.cursor()
        curs.execute(self.sql)
        self.end_time = datetime.now()
        
        cols = [x[0].lower() for x in curs.description]
        while(True):
            results = curs.fetchmany(25)
            if not results:
                break
            for r in results:
                if return_type  == 'dict':
                    yield dict(zip(cols,r))
                if return_type == 'rset':
                    yield r
            
    def exec_update(self, conn):
        self.start_time = datetime.now()
        curs = conn.cursor()
        curs.execute(self.sql)
        self.end_time = datetime.now()
        
        return curs.rowcount

    @staticmethod
    def bind(a):
        return str(a).replace("'", "''")


            
class Connection():
            
    def __init__(self, conn):
        self.conn = conn
        self.query_list = []
        
    def __str__(self):
        return str(self.conn)
    
    def select(self, from_clause, where = None, order = None, select_list = None):
        select_clause =  " * "
        if select_list:
            select_clause = ", ".join(select_list)
        
        order_by_clause = ""
        if order:
            order_by_clause = " order by " + order

        query = "select %s from %s %s %s" % (select_clause, from_clause, self.where_clause(where), order_by_clause)
        
        q = Query(query)
        self.query_list.append(q)
        return q.exec_select(self.conn)

    def select_sql(self, sql):
        q = query(sql)
        self.query_list.append(q)
        return q.exec_select(self.conn)

    def update(self, from_clause, set_list, where=None):
        set_clause = ", ".join(["%s = '%s'" % (x, self.bind(set_list[x])) for x in set_list.keys()])

        query = "update %s set %s %s" % (from_clause, set_clause, self.where_clause(where))
        
        q = Query(query)
        self.query_list.append(q)
        
        return q.exec_update(self.conn)
    
    def update_sql(self, sql):
        q = Query(sql)
        self.query_list.append(q)
        
        return q.exec_update(self.conn)
    
    def insert(self, from_clause, columns):
        column_list = ", ".join(columns.keys())
        value_list = "', '".join([columns[x] for x in columns.keys()])
        query = "insert into %s (%s) values ('%s')" % (from_clause, column_list, value_list)
        
        q = Query(query)
        self.query_list.append(q)
        
        return q.exec_update(self.conn)
    
    def upsert(self, from_clause, set_list, where):
        x = self.update(from_clause, set_list, where)
        if x == 0:
            x = self.insert(from_clause, set_list)
        return x
        
    def delete(self, from_clause, where):
        query = "delete from %s %s" % (from_clause, self.where_clause(where))
        q = Query(query)
        self.query_list.append(q)
        
        return q.exec_update(query)
    
    @staticmethod
    def where_clause(where):
        if not where:
            return ""

        if type(where) == type({}):
            return " where " + " and ".join(["%s = '%s'" % (x, Query.bind(where[x])) for x in where.keys()])

        if type(where) == type(""):
            return " where " + where
