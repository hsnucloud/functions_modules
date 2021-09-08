# -*- coding: utf-8 -*-
import sqlite3
from PyQt5.QtWidgets import *
import sys
import numpy as np

class SQL:
    def __init__(self,databasename,table = None):
        self.databasename = databasename
        self.defaulttable=table
        self.conn = sqlite3.connect('{}.db'.format(databasename))
        self.cur = self.conn.cursor()

    def createtable(self, collist, table):
        """
                ex :
                    collist : "( 'col1' UNIQUE PRIMARY KEY, ' col2',' col3')"
                """
        self.conn.execute('''CREATE table {}
                     {};'''.format(table, collist))
        return

    def update(self, collist, values, table = None):
        """
                ex:
                    collist :  "( col1,  col2, col3)"
                    values : "( 'string' , 'string2', number)"
                 """
        if table == None and self.defaulttable != None:
            table = self.defaulttable
        elif table == None and self.defaulttable == None:
            print("Didn't enter table")
            return
        self.cur.execute("INSERT OR REPLACE INTO {} {} \
                    VALUES {};".format(table, collist, values));
        self.conn.commit()
        return

    def addcol(self, colname, table = None):
        """
                ex:
                    colname="colname"
                """
        if table == None and self.defaulttable != None:
            table = self.defaulttable
        elif table == None and self.defaulttable == None:
            print("Didn't enter table")
            return
        self.conn.execute("ALTER TABLE {} ADD COLUMN {}".format(table, colname))
        self.conn.commit()
        return

    def getdata(self, con, colname='*', table = None):
        if table == None and self.defaulttable != None:
            table = self.defaulttable
        elif table == None and self.defaulttable == None:
            print("Didn't enter table")
            return
        self.cursor = self.conn.execute("SELECT {} FROM {} WHERE {}".format(colname, table, con))
        data = [tuple for tuple in self.cursor]
        try:
            return data
        except:
            return data

    def info(self, value=False, re=False, table = None):
        if table == None and self.defaulttable != None:
            table = self.defaulttable
            table_name_list=[table]
        elif table != None and table != "All":
            table_name_list = [table]
        elif table == "All" or self.defaulttable == None:
            table_name_list = [tuple[0] for tuple in
                               self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")]
        if re == False :
            print('Table name : \n', table_name_list)
        a = {}
        for i in table_name_list:
            self.cur.execute("SELECT * FROM {}".format(i))
            col_name_list = [tuple[0] for tuple in self.cur.description]
            data = self.conn.execute("SELECT * from {}".format(i))
            if re == False:
                print('Columns in {} : \n'.format(i), col_name_list)
            a.setdefault(i)
            a[i] = np.array([np.array(col_name_list)])
            if value == True:
                print('Value : ')
                for j in data:
                    print(list(j))
            if re == True:
                for k in data:
                    a[i] = np.append(a[i], [np.array(k)], axis=0)
                    #a[i].append(list(k))
        if re == True:
            return a
        else:
            return

    def colrename(self, oldcolname, newcolname, table = None):
        if table == None and self.defaulttable != None:
            table = self.defaulttable
        elif table == None and self.defaulttable == None:
            print("Didn't enter table")
            return
        Type = []
        NotNull = ['', 'NOT NULL']
        DefaultVal = []
        PrimaryKey = ['', 'PRIMARY KEY']

        self.cur.execute("SELECT * FROM {}".format(table))
        col_name_old = [tuple[0] for tuple in self.cur.description]
        i = col_name_old.index(oldcolname)
        col_name_new = list(col_name_old)
        col_name_new[i] = newcolname
        col_name_new = tuple(col_name_new)
        col_name_old = tuple(col_name_old)
        self. conn.execute("ALTER TABLE {} RENAME TO tmp_matel;".format(table))
        self.conn.execute("CREATE TABLE {} {}".format(table, str(col_name_new)))
        self.conn.execute("INSERT INTO {} {} SELECT * FROM tmp_matel;".format(table, str(col_name_new)))
        self.conn.execute("DROP TABLE tmp_matel;")
        self.conn.commit()
        return

    def deltable(self, tablename):
        self.conn.execute("DROP TABLE {};".format(tablename))
        #    conn.execute("ALTER TABLE {} RENAME TO matel;".format('tmp_matel'))
        #    conn.execute("DELETE from {} where {};".format(tablename,con))
        self.conn.commit()
        return

    def table(self,table = None):
        if table == None and self.defaulttable != None:
            table = self.defaulttable
        elif table == None and self.defaulttable == None:
            print("Didn't enter table")
            return
        app = QApplication(sys.argv)
        ex = TableEpitaxy(database = self.databasename, tablename=table)
        app.exec_()

    def close(self):
        self.conn.close()
        return


class TableEpitaxy(QTableWidget):
    def __init__(self,database,tablename):
        super().__init__()
        self.database=database
        self.tablename=tablename
        self.setupTable()
        self.initUI()

    def setupTable(self):
        database=SQL(self.database,self.tablename)
        data = database.info(re=True)
        data=data[self.tablename]
        Rows = len(data[0])
        Cols = len(data)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(Cols-1)
        self.tableWidget.setRowCount(Rows-1)

        self.HHL=[]
        for i in range(Cols-1):
            self.HHL.append(data[i+1][0])
        self.VHL=data[0][1:]
        self.tableWidget.setHorizontalHeaderLabels(self.HHL)
        self.tableWidget.setVerticalHeaderLabels(self.VHL)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #self.resizeColumnsToContents()
        for i in range(Cols-1):
            for j in range(Rows-1):
                self.tableWidget.setItem(j, i, QTableWidgetItem(str(data[i + 1][j + 1])))

    def initUI(self):
        self.setWindowTitle('{}-{}'.format(self.database,self.tablename))
        #self.setData(self.left, self.top, self.width, self.height)

        self.setupTable()

     # Add box layout, add table to box layout and add box layout to widget

        self.titleEdit = QTextEdit()
        self.titleEdit.setMinimumSize(100,100)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        #self.layout.addWidget(self.titleEdit)
        self.setLayout(self.layout)

        # Show widget
        self.show()




