# Use PyMySQL as MySQLdb if mysqlclient isn't available
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pass