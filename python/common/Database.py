# coding: utf-8
import uuid
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from common.Settings import Settings


class Database(object):

    def __init__(self):
        self.settings = Settings()
        self.env_vars = self.settings.getEnv()

    def createEngine(self):
        # 192.168.10.10
        connection_data = ('{connection}+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
            connection=self.env_vars["DB_CONNECTION"],
            username=self.env_vars["DB_USERNAME"],
            password=self.env_vars["DB_PASSWORD"],
            host=self.env_vars["DB_HOST"],
            port=self.env_vars["DB_PORT"],
            database=self.env_vars["DB_DATABASE"]
        ))

        # print "Connecting to database: %s" %(env_vars["DB_DATABASE"],)
        return create_engine(connection_data)

    def getValueFromTable(self, value, table, where):
        query = "select %s from %s where %s " % (value, table, where)
        result = self.createEngine().execute(query)
        for row in result:
            return row[0]

    def executeQuery(self, query):
        return self.createEngine().execute(query)

    def setValue(self, table_name, column, value, where_string):
        """Set a single value in a given table"""

        query = """
        UPDATE %s
        SET %s = '%s'
        %s
        """ % (table_name, column, value, where_string)
        self.executeQuery(query)

    def getValue(self, table_name, column, where_string):
        """Get a single value in a given table"""

        query = """
        SELECT %s from %s
        %s
        """ % (column, table_name, where_string)
        result = self.executeQuery(query)
        for row in result:
            return row[0]

    def getValues(self, table_name, columns, where_string=""):
        """Get multiple values from a given table"""

        query = """
        SELECT %s from %s
        %s
        """ % (columns, table_name, where_string)
        rows = []
        result = self.executeQuery(query)
        for row in result:
            rows.append(row)
        return rows

    def appendRows(self, table_name, dictionary):
        """Appends rows (a dict) to a table."""

        df = pd.DataFrame(data=dictionary).T

        df["created_at"] = datetime.now()
        df["updated_at"] = datetime.now()

        columns = self.getColumns(table_name)
        for column in columns:
            if column not in df.columns:
                df[column] = None

        df = df.reset_index(drop=True)
        df["id"] = pd.Series([uuid.uuid1() for i in range(len(df))]).astype(str)

        self.appendDataframe(table_name, df)

    def appendDataframe(self, table_name, df):
        """Write (append) a dataframe to the table specified"""
        # replacing inf with 0 to avoid this error explained here: https://github.com/PyMySQL/mysqlclient-python/issues/246
        df = df.replace([np.inf, -np.inf], 0)
        df.to_sql(table_name, self.createEngine(), if_exists='append', index=False)

    def getColumns(self, table_name):
        """Get the column names from a table. Returns a list"""

        query = """
        select COLUMN_NAME from (SELECT *
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = N'%s') as tb
        """ % (table_name)

        columns = None

        result = (Database()).executeQuery(query)

        for row in result:
            if not columns:
                columns = [row[0]]
            else:
                columns.append(row[0])

        if not columns:
            raise Exception("Could not determine columns from table %s" % (table_name))

        return columns
