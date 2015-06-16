import sqlite3 as sql


conn = None

try:
    conn = sql.connect('info.db')
    cur = conn.cursor()
    cur.executescript("""
        drop table if exists general_info;
        create table general_info(
            id integer primary key,
            system text,
            node text,
            platform text,
            cpu_usage real,
            virt_total real,
            virt_used real,
            virt_free real,
            virt_usage real);

        drop table if exists disk_info;
        create table disk_info(
            id integer,
            time text,
            partition text,
            total real,
            used real,
            free real,
            usage real);

        drop table if exists process_info;
        create table process_info(
            id integer,
            time text,
            pid integer,
            name text,
            username text,
            cpu_usage real,
            memory_usage real,
            threads integer);

        """)
    conn.commit()
    print("Script completed!")
except sql.Error as e:
    print("Error: ", e.args[0])

finally:
    if conn:
        conn.close()