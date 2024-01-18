FROM python:3.8-bullseye
ENV PYTHONUNBUFFERED 1
ENV LDAP_CRED $LDAP_CRED
WORKDIR /opt/ldap_auth
COPY requirements.txt /opt/ldap_auth/requirements.txt
COPY ldap_auth.py /opt/ldap_auth/ldap_auth.py
RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "/opt/ldap_auth/ldap_auth.py"]
