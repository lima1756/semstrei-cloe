import os
import cx_Oracle


class oracle_cx():

    connection_header_format = 'oracle+cx_oracle://{username}:{password}'
    tns_name_format = '(description= (retry_count={retry_count})(retry_delay={retry_delay})' +\
        '(address=(protocol={protocol})(port={port})(host={host}))' +\
        '(connect_data=(service_name={service_name}))' +\
        '(security=(ssl_server_cert_dn="{ssl_server_cert_dn}")))'

    def __init__(
        self,
        username,
        password,
        protocol,
        host,
        port,
        service_name,
        retry_count='20',
        retry_delay='3',
        ssl_server_cert_dn='CN=adwc.uscom-east-1.oraclecloud.com,OU=Oracle BMCS US,O=Oracle Corporation,L=Redwood City,ST=California,C=US'
    ):
        LD = os.getenv('LD_LIBRARY_PATH')
        cx_Oracle.init_oracle_client(lib_dir=LD)
        self.update_credentials(
            username,
            password,
            protocol,
            host,
            port,
            service_name,
            retry_count,
            retry_delay,
            ssl_server_cert_dn
        )

    def update_credentials(
        self,
        username,
        password,
        protocol,
        host,
        port,
        service_name,
        retry_count='20',
        retry_delay='3',
        ssl_server_cert_dn='CN=adwc.uscom-east-1.oraclecloud.com,OU=Oracle BMCS US,O=Oracle Corporation,L=Redwood City,ST=California,C=US'
    ):
        self.username = username
        self.password = password
        self.connection_header = self.__gen_connection_header__(
            username, password)
        self.tns_name = self.__gen_tns_name__(
            protocol, host, port, service_name, retry_count, retry_delay, ssl_server_cert_dn)
        self.connection_string = self.connection_header + '@' + self.tns_name

    def get_connection_string(self):
        return self.connection_string

    def __gen_connection_header__(
        self,
        username,
        password
    ):
        return self.connection_header_format.format(
            username=username,
            password=password
        )

    def __gen_tns_name__(
        self,
        protocol,
        host,
        port,
        service_name,
        retry_count,
        retry_delay,
        ssl_server_cert_dn
    ):
        return self.tns_name_format.format(
            protocol=protocol,
            host=host,
            port=port,
            service_name=service_name,
            retry_count=retry_count,
            retry_delay=retry_delay,
            ssl_server_cert_dn=ssl_server_cert_dn
        )

    def get_oracle_connection(self, tns_name_ora):
        """
            Requires $LD_LIBRARY_PATH/network/admin to have oracle wallet
        """
        cx_Oracle.connect(self.username, self.password, tns_name_ora)
