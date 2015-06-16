import sqlite3 as sql
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--table", help="What table you want to query: general, partition, process or all", required=True)
parser.add_argument("-f", "--first", help="First n rows", type=int)
parser.add_argument("-id", "--id", help="Show results that have this id", type=int)
args = vars(parser.parse_args())
query_table = args["table"]


order = ""
table = ""
if query_table == "general":
    table = "general_info"
    order = "order by node"

elif query_table == "partition":
    table = "disk_info"
    order = "order by id, time"

elif query_table == "process":
    table = "process_info"
    order = "order by id, time"

elif query_table == "all":
    table = "general_info g, disk_info d, process_info p"
    order = "order by d.time"

else:
    print("Wrong query")
    exit()


stm = "select * from " + table

ids = args["id"]
if ids:
    i = str(ids)
    if query_table == "all":
        stm += " where g.id = " + i + " and d.id = " + i + " and p.id = " + i
    else:
        stm += " where id = " + i

stm += " " + order

nr = args["first"]
if nr:
    stm += " LIMIT " + str(nr)


conn = None
try:
    conn = sql.connect('info.db')
    cur = conn.cursor()
    stm += ";"
    cur.execute(stm)
    rows = cur.fetchall()
    for row in rows:
        print(row)
        print("\n")

except sql.Error as e:
    print("SQL Error: ", e.args[0])
finally:
    if conn:
        conn.close()