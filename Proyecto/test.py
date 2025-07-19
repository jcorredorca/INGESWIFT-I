'''Modulo de test'''
import unittest
from services.login import autenticar_credenciales, hash_contrasena
from services.funcionario import registrar_miembro, eliminar_miembro

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

if __name__ == '__main__':
    unittest.main()
