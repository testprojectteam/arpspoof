import MySQLdb
class db:
    def __init__(self,host,user,password,dbname):
        self.db = MySQLdb.connect(host,user,password,dbname)
        self.cursor = self.db.cursor()
        # self.data = self.cursor.execute("SELECT VERSION()");
        # print "%s" % self.data
        self.cursor.execute("DROP TABLE IF EXISTS arp_map")
        self.sql = """ CREATE TABLE  arp_map (
            IP CHAR(20) NOT NULL ,
            MAC CHAR(40) NOT NULL,
            IP_MAC CHAR(60) NOT NULL,
            PRIMARY KEY (IP_MAC)
        ) """# self.cursor.execute("DROP TABLE IF EXISTS arp_map")# self.cursor.execute("DROP TABLE IF EXISTS arp_map")
        try:
            self.cursor.execute(self.sql)
            self.db.commit()
        except:
            print "Error creating table"

        self.cursor.execute("DROP TABLE IF EXISTS inv_host")
        self.sql = """ CREATE TABLE inv_host (
            IP CHAR(20) NOT NULL ,
            MAC CHAR(40) NOT NULL,
            IP_MAC CHAR(60) NOT NULL,
            PRIMARY KEY(IP_MAC)
        ) """
        try:
            self.cursor.execute(self.sql)
            self.db.commit()
        except:
            print "Error creating table"

    def get_mac(self,ip):
        self.sql="""SELECT MAC FROM arp_map
                        WHERE IP ='%s'""" % (ip)
        try:
            self.cursor.execute(self.sql);
        except:
            print "cannot fetch entries from table"
        return self.cursor.fetchone()[0];

    def get_ip(self,mac):
        self.sql="""SELECT IP FROM arp_map
                        WHERE MAC ='%s'""" % (mac)
        try:
            self.cursor.execute(self.sql);
        except:
            print "cannot fetch entries from table"
        return self.cursor.fetchone()[0];
    def update_ip(self,ip,mac):
        self.sql="""UPDATE arp_map SET IP = '%s' WHERE MAC = '%s'""" % (ip,mac)
        try:
            self.cursor.execute(self.sql)
            self.db.commit()
        except:
            print "error updating"
    def add_info(self,ip,mac,ip_mac):
        self.sql="""INSERT INTO arp_map (IP,MAC,IP_MAC) VALUES ('%s','%s','%s')""" % (ip,mac,ip_mac)

        try:
            self.cursor.execute(self.sql)
            self.db.commit()
        except:
            print "error"

    def add_info_inv(self,ip,mac,ip_mac):
        self.sql="""INSERT INTO inv_host (IP,MAC,IP_MAC) VALUES ('%s','%s','%s')""" % (ip,mac,ip_mac)
        try:
            self.cursor.execute(self.sql)
            self.db.commit()
        except:
            print "Entry already in db"

    def present(self,ip_mac):
        self.sql="""SELECT * FROM arp_map
                        WHERE IP_MAC='%s'""" % (ip_mac)
        try:
            self.cursor.execute(self.sql)
        except:
            print "error fetching data from db"
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def present_mac(self,mac):
        self.sql="""SELECT * FROM arp_map
                        WHERE MAC='%s'""" % (mac)
        try:
            self.cursor.execute(self.sql)
        except:
            print "error fetching data from db"
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def return_table(self):
        self.sql = "SELECT * FROM arp_map"
        self.cursor.execute(self.sql)
        # try:
        #
        # except:
        #     print "error fetching data from db"
        #     return ""
        return self.cursor.fetchall()

    def return_table_inv(self):
        self.sql = "SELECT * FROM inv_host"
        self.cursor.execute(self.sql)
        # try:
        #
        # except:
        #     print "error fetching data from db"
        #     return ""
        return self.cursor.fetchall()
