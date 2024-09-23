from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
from models.usuario import usuario

class conexionDA:
    @staticmethod
    def ObtenerRegistroDA(registro):
        try:
            # Configura el servidor con un tiempo de espera de conexión de 10 segundos
            server = Server('ldap://10.1.141.25', get_info=ALL, connect_timeout=10)
            print("Servidor configurado correctamente")

            # Conecta al servidor LDAP
            conn = Connection(server, user='c1395673@ecopetrol.com.co', password='*PkiNfpSZ2y*', auto_bind=True, auto_referrals=False)
            print(f"Conexión establecida: {conn.bound}")

            # Base DN
            base_dn = 'ou=Colombia,dc=red,dc=ecopetrol,dc=com,dc=co'
            
            # Filtro de búsqueda por registro
            search_filter = f'(sAMAccountName={registro})'
            
            # Atributos a recuperar
            attributes = ['sAMAccountName', 'cn', 'givenName', 'mail']

            # Realiza una búsqueda
            conn.search(base_dn, search_filter, attributes=attributes, search_scope=SUBTREE)
            print(f"¿Búsqueda exitosa?: {conn.result['description']}")
            print(f"Número de entradas encontradas: {len(conn.entries)}")

            # Si hay resultados, imprímelos
            if conn.entries:
                # Accede a la entrada deseada
                entry = conn.entries[0]

                return usuario(
                    nombre=entry.cn.value,
                    correo=entry.mail.value,
                    registro=entry.sAMAccountName.value
                )

            else:
            
                return 'usuario no encontrado en la base de datos ni en el directorio activo'

        except LDAPException as e:
            print(f"Error en la conexión o búsqueda LDAP: {e}")
        except Exception as e:
            print(f"Error general: {e}")
