'''Modulo de test'''
import unittest
from datetime import datetime

from models import FuncionariosEnSesion, SessionLocal
from services import administrador
from services.funcionario import eliminar_miembro, registrar_miembro
from services.login import (autenticar_credenciales, cambiar_contrasena,
                            hash_contrasena)


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

#jcorredorca
class TestAdministrador(unittest.TestCase):
    '''Tests relacionados con las funcionalidades del administrador'''

    def test_crear_horario(self):
        '''Verifica que al crear un horario se retorne un ID válido'''
        publico = 'FUNCIONARIO'
        fecha = datetime(2025, 7, 20, 10, 0)
        actividad = 'TALLER'

        ubicaciones = administrador.recuperar_ubicaciones()
        self.assertTrue(ubicaciones, msg="No hay ubicaciones registradas")

        id_ubicacion = administrador.recuperar_id_ubicacion(ubicaciones[0])
        parametros = [publico, fecha, actividad, id_ubicacion]

        id_sesion = administrador.crear_horario(parametros)
        self.assertIsNotNone(id_sesion)
        self.assertGreater(id_sesion, 0)

        administrador.eliminar_sesion(id_sesion)

    def test_asignar_funcionarios_a_sesion(self):
        '''Verifica que se asignen correctamente funcionarios y profesor a una sesión'''
        # Crear sesión temporal
        ubicaciones = administrador.recuperar_ubicaciones()
        id_ubicacion = administrador.recuperar_id_ubicacion(ubicaciones[0])
        fecha = datetime(2025, 7, 21, 9, 0)
        id_sesion = administrador.crear_horario(['GENERAL', fecha, 'PRUEBA', id_ubicacion])

        funcionarios = administrador.recuperar_funcionarios()
        self.assertGreaterEqual(len(funcionarios),
                                2,
                                msg="Se requieren al menos 2 funcionarios para esta prueba")

        ids_funcionarios = [f[1] for f in funcionarios[:2]]
        profesor = ids_funcionarios[0]
        resto = [ids_funcionarios[1]]

        administrador.asignar_funcionarios(resto, id_sesion, profesor)

        # Verificar que los 2 registros están presentes
        with SessionLocal() as session:
            count = session.query(FuncionariosEnSesion).filter(
                FuncionariosEnSesion.sesiones_id == id_sesion
            ).count()

        self.assertEqual(count, 2)

        # Limpieza
        administrador.eliminar_sesion(id_sesion)

    def test_actualizar_publico_y_ubicacion(self):
        '''Verifica que se actualice correctamente el público y la ubicación de una sesión'''
        ubicaciones = administrador.recuperar_ubicaciones()
        id_ubicacion_inicial = administrador.recuperar_id_ubicacion(ubicaciones[0])
        fecha = datetime(2025, 7, 22, 11, 0)
        id_sesion = administrador.crear_horario(['GENERAL',
                                                 fecha,
                                                 'ENTRENAMIENTO',
                                                 id_ubicacion_inicial])

        ubicacion_nueva = ubicaciones[-1] if len(ubicaciones) > 1 else ubicaciones[0]
        nuevo_publico = 'FODUN'

        administrador.actualizar_publico_ubicacion(id_sesion, nuevo_publico, ubicacion_nueva)

        resultado = administrador.recuperar_ubicacion_publico(id_sesion)
        self.assertEqual(resultado[0], nuevo_publico)
        self.assertEqual(resultado[1], ubicacion_nueva)

        # Limpieza
        administrador.eliminar_sesion(id_sesion)


if __name__ == '__main__':
    unittest.main()

#lalvarezla
class TestFuncionario(unittest.TestCase):
    '''Tests relacionados con la gestión de funcionarios'''

    def test_registro_miembro_exitoso(self):
        '''Verifica que un miembro se registre correctamente'''
        user = 'nuevo_test'
        contrasenia = 'clave123'
        info_miembro = {
            "usuario": user,
            "nombre": 'Nombre',
            "apellido": 'Apellido',
            "contrasena": hash_contrasena(contrasenia),
            "correo": 'nuevo@unal.edu.co',
            "rol": 'Estudiante',
            "programa": 'Ingeniería'
        }

        registrar_miembro(info_miembro)
        # Verificar que se pueda autenticar
        self.assertTrue(autenticar_credenciales(user, contrasenia))
        eliminar_miembro(user)

    def test_registro_usuario_duplicado(self):
        '''Verifica que no se permita registrar un usuario ya existente'''
        user = 'duplicado_test'
        contrasenia = 'clave123'
        info_miembro = {
            "usuario": user,
            "nombre": 'Nombre',
            "apellido": 'Apellido',
            "contrasena": hash_contrasena(contrasenia),
            "correo": 'repetido@unal.edu.co',
            "rol": 'Estudiante',
            "programa": 'Ingeniería'
        }

        registrar_miembro(info_miembro)
        with self.assertRaises(ValueError) as context:
            registrar_miembro(info_miembro)

        self.assertIn("ya existe", str(context.exception).lower())
        eliminar_miembro(user)

    def test_eliminar_usuario_inexistente(self):
        '''Verifica el comportamiento al intentar eliminar un usuario inexistente'''
        with self.assertRaises(ValueError) as context:
            eliminar_miembro('usuario_inexistente')
        self.assertIn("no existe", str(context.exception).lower())
