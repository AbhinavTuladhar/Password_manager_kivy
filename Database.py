"""
Everything database-related is in here!
"""
from sqlalchemy import (
    create_engine, 
    MetaData,
    select,
    update,
    Table, Column,
    Integer, String,
    delete
)
import pandas as pd
from AES import AESEncryptor
from utils import string_to_bytes, bytes_to_string


class Connection:
    def __init__(self):
        self.engine = create_engine("sqlite:///password.db")
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.create_tables()
        
    def create_tables(self) -> None:
        """
        Create the table.
        
        If the table already exists, then nothing is done.
        """
        self.websites = Table(
            'websites', self.metadata,
            Column('ID', Integer(), primary_key=True),
            Column('website', String()),
            Column('URL', String()),
            Column('email', String()),
            Column('username', String()),
            Column('password', String())
        )
        self.metadata.create_all(self.engine)
        
    def insert_data_from_input(self, data: dict) -> None:
        """
        Insert rows into the table from the dictionary `data`.
        
        Args:
            data: A dictionary containing the information to be inserted into the database.
            AES: An AESEncryption object which contains the master password passed to it.
            
        Returns:
            None.
        """
        # Empty string = NULL value.
        for key, item in data.items():
            if item == '':
                data[key] = None
        
        ins = self.websites.insert()
        self.connection.execute(ins, data)
        print("Data has successfully been inserted into the database!")
        
    def update_passwords(self, AES1: AESEncryptor, AES2: AESEncryptor) -> None:
        """
        Update the passwords in the database when the master password is updated.
        
        Args:
            AES1: The encryptor which takes the old master password.
            AES2: The encryptor which takes the updated master password.
        """    
        query = select([self.websites.c.ID, self.websites.c.password])
        proxy = self.connection.execute(query)
        results = proxy.fetchall()
        
        ID_numbers = []
        original_passwords = []
        new_passwords = []
        
        for row in results:
            ID_numbers.append(row[0])
            original_passwords.append(row[1])
            
        for ID, password in zip(ID_numbers, original_passwords):
            # Decrypt the stored password using the original master password.
            password_byte = string_to_bytes(password)
            old_decrypted_password = AES1.decrypt(password_byte)
            
            # Then encrypt the password using the new master password.
            new_encrypted_password_bytes = AES2.encrypt(old_decrypted_password)
            new_encrypted_password = bytes_to_string(new_encrypted_password_bytes)
            new_passwords.append(new_encrypted_password)
            
            query = update(self.websites).where(self.websites.c.ID == ID)
            query = query.values(
                password=new_encrypted_password
            )
            self.connection.execute(query)
            
    def update_all_information(self, ID: int, data: dict) -> None:
        """
        Update all the records of the webites having ID `ID` with data contained in the dictionary `data`.
        
        Args:
            ID: The ID of the website to be updated
            data: A dictionary containing the information to be updated.
        """
        query = update(self.websites) \
            .where(self.websites.c.ID == ID) \
            .values(data)
        self.connection.execute(query)
        
    def get_information(self, id: int,website: str) -> tuple:
        """
        Gets login information of `website`.
        
        Args:
            website: The name of the website. Needs to be an exact match.
            
        Return:
            A tuple containing all the details of `website.`
        """
        query = select([self.websites])
        query = query.where(self.websites.c.ID == id)
        query = query.where(self.websites.c.website == website)
        proxy = self.connection.execute(query)
        row = proxy.fetchone()
        return row
    
    def delete_entry(self, id: int, website_name: str) -> None:
        """
        Delete the rows having an ID of `id` with a website of `website_name`.
        
        Arguments:
            id: The primary key of the row
            website_name: The name of the website.
        """
        query = delete(self.websites).where(self.websites.c.ID == id)
        query = query.where(self.websites.c.website == website_name)
        result = self.connection.execute(query)

    
    def get_website_names(self) -> list:
        """
        Returns the name of all the website names that are in the database.
        
        Returns:
            A list of the website names.
        """
        query = select([self.websites.c.ID, self.websites.c.website])
        proxy = self.connection.execute(query)
        rows = proxy.fetchall()
        website_names = []
        for row in rows:
            website_names.append([str(row[0]), row[1]])
        return website_names
