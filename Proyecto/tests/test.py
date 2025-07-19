'''Modulo de test'''
import unittest
from services.login import autenticar_credenciales, hash_contrasena, cambiar_contrasena
from services.administrador import activar_miembros, desactivar_miembros
from services.funcionario import registrar_miembro, eliminar_miembro
from services.miembros import recuperar_estado

#sfetecua
class TestLogin(unittest.TestCase):
    '''Tests relacionados a la validacion de contrasenia'''

    def test_contrasenia_correcta(self):
        '''Revisa comportamiento esperado para una contrasenia correcta'''
        # Given: un miembro
        user = 'test0'
        contrasenia = 'ejemplo123'

        info_miembro = {
                "usuario": user,
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena(contrasenia),
                "correo": 'sfetecua@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro)

        # When: se coloca la contrasenia adecuada
        # Then: debe ser posible su ingreso
        self.assertTrue(autenticar_credenciales(user, contrasenia),
                                                msg='La utenticacion, caso correcto no es adecuada')

        eliminar_miembro('test0')

    def test_contrasenia_incorrecta(self):
        '''Revisa comportamiento esperado para una contrasenia incorrecta'''
        # Given: un miembro
        user = 'test0'
        contrasenia = 'ejemplo123'

        info_miembro = {
                "usuario": user,
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena(contrasenia),
                "correo": 'sfetecua@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro)

        # When: se coloca la contrasenia incorrecta
        contrasenia = 'banana'
        # Then: no debe ser posible su ingreso
        with self.assertRaises(ValueError,
                                msg='La utenticacion, caso incorrecto no es adecuada'
                                ) as context:
            autenticar_credenciales(user, contrasenia)

         # Verificar que el mensaje sea exactamente el esperado
        self.assertEqual(
                        str(context.exception),
                         "El usuario o contraseña ingresado no son correctos."
                         )

        eliminar_miembro('test0')

    def test_usuario_inexistente(self):
        '''Revisa comportamiento esperado para un usuario inexistente'''
        # Given: un miembro inexistente
        user = 'test0'

        # When: se trata de ingr)suario
        contrasenia = 'banana'
        # Then: no debe ser posible su ingreso
        with self.assertRaises(ValueError,
                                msg='La utenticacion, caso incorrecto no es adecuada'
                                ) as context:
            autenticar_credenciales(user, contrasenia)

         # Verificar que el mensaje sea exactamente el esperado
        self.assertEqual(
                        str(context.exception),
                         "El usuario o contraseña ingresado no son correctos."
                         )

#nbolanosf
class TestCambioContrasenia(unittest.TestCase):
    '''Tests realcionados al cambio de contrasenia'''

    def test_cambio_exitoso(self):
        '''Verifica que el cambio de contraseña se realice de forma exitosa'''
        #Given: Un usuario con credenciales válidas
        user = 'cambio'
        contrasenia = 'contrasenia'

        info_miembro = {
                "usuario": user,
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena(contrasenia),
                "correo": 'nbolanosf@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro)

        #When: Cambia su contrasenia
        nueva_contrasenia = 'exitoso'
        cambiar_contrasena(user, nueva_contrasenia)

        #Then: El usuario accede con sus nuevas credenciales
        self.assertTrue(autenticar_credenciales(user, nueva_contrasenia),
                                                msg='La contraseña no se actualizó')

        eliminar_miembro('cambio')

    def test_contrasenia_antigua_inutil(self):
        '''Verifica que al cambiar la contrasenia, las credenciales anteriores no funcionen'''
        #Given: Un usuario con credenciales válidas
        user = 'cambio'
        contrasenia_vieja = 'contrasenia'

        info_miembro = {
                "usuario": user,
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena(contrasenia_vieja),
                "correo": 'nbolanosf@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro)

        #When: Cambia su contrasenia
        nueva_contrasenia = 'exitoso'
        cambiar_contrasena(user, nueva_contrasenia)

        #Then: El usuario accede con sus nuevas credenciales
        self.assertRaises(ValueError, autenticar_credenciales, user, contrasenia_vieja)

        eliminar_miembro('cambio')

#nbolanosf
class TestRecuperarEstado(unittest.TestCase):
    '''Tests relacionados a la recuperación del estado de un miembro'''

    def test_miembro_nuevo_inactivo(self):
        '''Verifica que un mimebro recién registrado aparezca inactivo'''
        #Given: Un miembro recién registrado

        info_miembro1 = {
                "usuario": '1',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf@unal.edu.co',
                "rol": None,
                "programa": None,
            }

        #When: Se registra por primera vez en el sistema
        registrar_miembro(info_miembro1)

        #Then: El usuario estpa inactivo
        self.assertTrue(recuperar_estado('1') == 'INACTIVO', msg='No se crean miembros inactivos')

        eliminar_miembro('1')

    def test_miembro_activo(self):
        '''Verifica que un mimebro recién registrado aparezca inactivo'''
        #Given: Un miembro

        info_miembro1 = {
                "usuario": '1',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro1)

        #When: Se activa
        activar_miembros(['1'])

        #Then: El usuario '1' está activo y '2' permanece inactivo
        self.assertTrue(recuperar_estado('1') == 'ACTIVO', msg='No se activó a 1')

        eliminar_miembro('1')

#nbolanosf
class TestActivaryDesactivarMiembros(unittest.TestCase):
    '''Tests asociados al camb io de estado de miembros'''

    def test_activar_miembros(self):
        '''Verifica que una lista de miembros se active correctamente'''
        #Given: 2 miembros registrados (inactivos)
        info_miembro1 = {
                "usuario": '1',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf1@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        info_miembro2 = {
                "usuario": '2',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf2@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        registrar_miembro(info_miembro1)
        registrar_miembro(info_miembro2)

        #When: Se activa solo el que se indica
        activar_miembros(['1'])

        #Then: Los miembros '1' y '2' están activos
        self.assertTrue(recuperar_estado('1') == 'ACTIVO',
                        msg='No se activó un miembro solicitado')
        self.assertTrue(recuperar_estado('2') == 'INACTIVO',
                        msg='Se activó erroneamente a un miembro no solicitado')

        eliminar_miembro('1')
        eliminar_miembro('2')

    def test_multiples_operaciones(self):
        '''Verifica que indique correctamente el estado de los miembros'''
        #Given: Tres miembros

        info_miembro1 = {
                "usuario": '1',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf1@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        info_miembro2 = {
                "usuario": '2',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf2@unal.edu.co',
                "rol": None,
                "programa": None,
            }
        info_miembro3 = {
                "usuario": '3',
                "nombre": 'nombre',
                "apellido": 'apellido',
                "contrasena": hash_contrasena('1'),
                "correo": 'nbolanosf3@unal.edu.co',
                "rol": None,
                "programa": None,
            }

        registrar_miembro(info_miembro1)
        registrar_miembro(info_miembro2)
        registrar_miembro(info_miembro3)

        #When: Cambian sus estados entre ACTIVO e INACTIVO
        activar_miembros(['1', '2', '3'])
        desactivar_miembros(['2', '3'])
        activar_miembros(['3'])

        #Then: Cada usuario corresponde con su estado
        self.assertTrue(recuperar_estado('1') == 'ACTIVO', msg='No se activó el miembro 1')
        self.assertTrue(recuperar_estado('2') == 'INACTIVO', msg='No se desactivó al miembro 2')
        self.assertTrue(recuperar_estado('3') == 'ACTIVO', msg='No se reactivó al miembro 3')

        eliminar_miembro('1')
        eliminar_miembro('2')
        eliminar_miembro('3')


if __name__ == '__main__':
    unittest.main()
