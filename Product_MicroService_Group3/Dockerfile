FROM python:3.11.4

#Copy requirements
COPY requirements.txt /product_ms/

COPY app /product_ms/

#Set working direcroty
WORKDIR /product_ms

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Install other libraries in container
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
	iputils-ping\
	apt-transport-https \
	gcc\
    curl \
    gnupg \
    freetds-dev \
    tdsodbc \
    && rm -rf /var/lib/apt/lists/*


#Install ODBC Driver for Microsoft SQL Server Section...
#Source: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

	
#Add Microsoft repository GPG key
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

#Add the Microsoft SQL Server repository for Debian 12
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list


#Add Microsoft GPG key
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-archive-keyring.gpg

#Add the Microsoft SQL Server repository for Debian 12
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list

#Update package list
RUN apt-get update

#Install ODBC Driver 17 for SQL Server
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

#Install mssql-tools
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN bash -c "echo 'export PATH=\"$PATH:/opt/mssql-tools/bin\"' >> ~/.bashrc && source ~/.bashrc"


#RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && source ~/.bashrc


RUN apt-get install -y libgssapi-krb5-2


#Set environment variables for ODBC configuration
ENV ODBCINI=/etc/odbc.ini
ENV ODBCSYSINI=/etc

CMD ["python", "index.py"]