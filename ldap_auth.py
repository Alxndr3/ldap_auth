import ldap
import os


def check_credentials(ldap_username, ldap_password, ldap_server):
    """
    Verifies credentials for username, password and certificate.
    """

    base_dn = "DC=mycorp,DC=corp"
    ldap_filter = f"sAMAccountName=alexandre" # retrieve info from user alexandre
    ldap_server = "ldaps://ad1.mycorp.corp"
    search_attribute = ["memberOf"]


    try:
        ldap_client = ldap.initialize(ldap_server)
        # Set LDAP protocol version used
        ldap_client.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        # Force cert validation
        ldap_client.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        # Set path name of file containing all trusted CA certificates
        ldap_client.set_option(ldap.OPT_X_TLS_CACERTFILE, cacertfile)
        # Force libldap to create a new SSL context (must be last TLS option!)
        ldap_client.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
        # int specifying whether referrals should be automatically chased within the underlying LDAP C lib
        ldap_client.set_option(ldap.OPT_REFERRALS, 0)
        # perform a synchronous bind
        ldap_client.simple_bind_s(ldap_username, ldap_password)
        # query = ldap_client.search_s(BASE_DN, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1][0]
        query = ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter,
                                     search_attribute)[0]
        ldap_client.unbind()
        return query
    except ldap.INVALID_CREDENTIALS as e:
        ldap_client.unbind()
        return f"Invalid username or password: {e}"
    except ldap.SERVER_DOWN:
        return "AD server not available."
    except Exception as e:
        ldap_client.unbind()
        return f'An unexpected error occurred: {e}'


cacertfile = "./ca-mycorp.corp.crt"
ldap_username = "alexandre@mycorp.corp"
ldap_password = os.environ.get("LDAP_CRED")

print(check_credentials(ldap_username, ldap_password, cacertfile))

