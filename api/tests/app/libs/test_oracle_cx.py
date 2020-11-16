import unittest
import json
import cx_Oracle
import logging

from app.libs import oracle_cx
from ..base_test_app import BaseTestApp


class TestOracleCX(BaseTestApp):

    connection = oracle_cx(
        "test_user",
        "Test_password123",
        "tcp",
        "localhost",
        "9912",
        "database"
    )
    expected_header = 'oracle+cx_oracle://test_user:Test_password123'
    expected_tns = '(description= (retry_count=20)(retry_delay=3)' +\
        '(address=(protocol=tcp)(port=9912)(host=localhost))' +\
        '(connect_data=(service_name=database))' +\
        '(security=(ssl_server_cert_dn="CN=adwc.uscom-east-1.oraclecloud.com,OU=Oracle BMCS US,O=Oracle Corporation,L=Redwood City,ST=California,C=US")))'

    def test_connection_header(self):
        self.assertTrue(self.connection.connection_header ==
                        self.expected_header)

    def test_tns(self):
        self.assertTrue(self.connection.tns_name == self.expected_tns)

    def test_connection_string(self):
        self.assertTrue(self.connection.get_connection_string() ==
                        self.expected_header+'@'+self.expected_tns)

    def test_oracle_default_connection(self):
        try:
            oracle_connection = self.connection.get_oracle_default_connection(
                'test_name')
            cursor = oracle_connection.cursor()
            result = cursor.execute("select dummy from dual")
            for row in result:
                self.assertTrue(row[0] == 'X')
        except cx_Oracle.DatabaseError:
            logging.error(
                "Couldn't resolve TNS, probably wallet hasn't been added to OracleClient/network/admin Please look at the readme project")
