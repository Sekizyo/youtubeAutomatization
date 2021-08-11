import os
import sqlite3
from sqlite3 import Error

class databaseManager():
  def __init__(self):
    self.databasePath = 'modules/storage/database.sqlite'
    self.initCheck()
    self.connection = self.createConnection()

  def initCheck(self):
    if not os.path.isfile(self.databasePath):
      database = open(self.databasePath, 'x')
      database.close()

    self.connection = self.createConnection()

    self.createAuthorTableQuery()
    self.createVideoTableQuery()

    self.closeConnection()

  def createConnection(self):
    connection = None
    try:
      connection = sqlite3.connect(self.databasePath)
      print("Connection to SQLite DB successful")

    except Error as e:
      raise

    return connection

  def closeConnection(self):
    try:
      if self.connection:
        self.connection.close()

    except Error as e:
      raise

  def createVideoTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS videos(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      authorID INTEGER,
      title TEXT NOT NULL,
      description TEXT,
      uploaded BOOL NOT NULL,
      rendered BOOL NOT NULL,
      path TEXT NOT NULL,
      pathThumbnail TEXT NOT NULL,
      soundcloudLink TEXT NOT NULL
      );
      """
      
    response = self.executeQuery(query)
    return response

  def createAuthorTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS author(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      soundcloudLink TEXT NOT NULL
      );
      """

    response = self.executeQuery(query)
    return response

  def selectQuery(self, data, table, condition='1'):
    query = f'SELECT {"".join(data)} FROM {table} WHERE {condition};'

    response = self.executeQuery(query)
    return response

  def insertIntoQuery(self, tableName, columns, values):
    query = f'INSERT INTO {tableName} ({", ".join(columns)}) VALUES ({", ".join(values)});'
    
    response = self.executeQuery(query)
    return response

  def updateRecordQuery(self, tableName, column, value, condition):
    query = f'UPDATE {tableName} SET {column} = {value} WHERE {condition};'
    
    response = self.executeQuery(query)
    return response

  def updateRecordByIDQuery(self, tableName, column, value, ID):
    response = self.updateRecordQuery(tableName, column, value, f'ID = {ID}')
    return response 

  def deleteFromTableQuery(self, tableName, condition):
    query = f'DELETE FROM {tableName} WHERE {condition};'
    
    response = self.executeQuery(query)
    return response

  def dropTabletQuery(self, tableName):
    query = f'DROP TABLE {tableName};'

    response = self.executeQuery(query)
    return response

  def executeQuery(self, query):
    cursor = self.connection.cursor()

    try:
      response = cursor.execute(query).fetchall()

      self.connection.commit()

      if response:
        return response
      else:
        return None

    except:
      raise

  def __del__(self):
    self.closeConnection()
