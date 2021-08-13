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

    self.createAudioTableQuery()
    self.createImageTableQuery()
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

  def createAudioTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS audio(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      authorName TEXT NOT NULL,
      creds TEXT NOT NULL,
      rendered BOOL NOT NULL DEFAULT false,
      UNIQUE(title)
      );
      """

    response = self.executeQuery(query)
    return response

  def createImageTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS image(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      filename TEXT NOT NULL,
      creds TEXT NOT NULL,
      rendered BOOL NOT NULL DEFAULT false,
      UNIQUE(filename)
      );
      """
    
    response = self.executeQuery(query)
    return response

  def createVideoTableQuery(self): #TODO FOR NEXT SESSION create new way for uploader to get info from video, needs video needs new author column or query from audio author
    query = f"""CREATE TABLE IF NOT EXISTS video(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      audioID INTEGER NOT NULL,
      thumbnailID INTEGER NOT NULL,
      title TEXT NOT NULL,
      rendered BOOL NOT NULL DEFAULT false,
      uploaded BOOL NOT NULL DEFAULT false,
      UNIQUE(title)
      );
      """

    response = self.executeQuery(query)
    return response

  def selectQuery(self, data, table, condition='1'):
    query = f'SELECT {"".join(data)} FROM {table} WHERE {condition};'

    response = self.executeQuery(query)
    return response

  def selectLimit1Query(self, data, table, condition='1'):
    response = self.selectQuery(data, table, condition + ' LIMIT 1')
    return response

  def insertIntoQuery(self, tableName, columns, values):
    query = f'INSERT INTO {tableName} ({columns}) VALUES ({values});'

    response = self.executeQuery(query)
    return response

  def updateRecordQuery(self, tableName, column, value, condition):
    query = f'UPDATE {tableName} SET {column} = {value} WHERE {condition};'
    
    response = self.executeQuery(query)
    return response

  def updateRecordByIDQuery(self, tableName, column, value, ID):
    response = self.updateRecordQuery(tableName, column, value, f'ID == {ID}')
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

    except:
      raise

  def __del__(self):
    self.closeConnection()
