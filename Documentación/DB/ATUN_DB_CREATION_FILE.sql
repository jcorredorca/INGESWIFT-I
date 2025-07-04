DROP SCHEMA IF EXISTS `AFID` ;

-- -----------------------------------------------------
-- Schema AFID
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `AFID` DEFAULT CHARACTER SET utf8 ;
USE `AFID` ;

-- -----------------------------------------------------
-- Table `AFID`.`personas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`personas` ;

CREATE TABLE IF NOT EXISTS `AFID`.`personas` (
  `usuario` VARCHAR(15) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `apellido` VARCHAR(45) NOT NULL,
  `hash_contrasena` VARCHAR(255) NOT NULL,
  `estado` ENUM('ACTIVO', 'INACTIVO') NULL DEFAULT 'INACTIVO',
  `correo` VARCHAR(45) NOT NULL,
  `rol_en_universidad` ENUM('GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO') NULL,
  `grupo_especial` ENUM('JOVENES', 'SELECCION') NULL,
  PRIMARY KEY (`usuario`),
  UNIQUE INDEX `hash_correo_UNIQUE` (`usuario` ASC) VISIBLE,
  UNIQUE INDEX `correo_UNIQUE` (`correo` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`actividad`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`actividad` ;

CREATE TABLE IF NOT EXISTS `AFID`.`actividad` (
  `tipo` VARCHAR(45) NOT NULL,
  `aforo` TINYINT NOT NULL,
  PRIMARY KEY (`tipo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`ubicaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`ubicaciones` ;

CREATE TABLE IF NOT EXISTS `AFID`.`ubicaciones` (
  `id_ubicaciones` INT NOT NULL AUTO_INCREMENT,
  `ubicacion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_ubicaciones`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`sesiones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`sesiones` ;

CREATE TABLE IF NOT EXISTS `AFID`.`sesiones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `publico` ENUM('GENERAL', 'FUNCIONARIOS', 'FODUN') NOT NULL,
  `fecha` DATETIME NOT NULL,
  `actividad_tipo` VARCHAR(45) NOT NULL,
  `ubicaciones_id_ubicaciones` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sesiones_actividad1_idx` (`actividad_tipo` ASC) VISIBLE,
  INDEX `fk_sesiones_salones1_idx` (`ubicaciones_id_ubicaciones` ASC) VISIBLE,
  CONSTRAINT `fk_sesiones_actividad1`
    FOREIGN KEY (`actividad_tipo`)
    REFERENCES `AFID`.`actividad` (`tipo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sesiones_salones1`
    FOREIGN KEY (`ubicaciones_id_ubicaciones`)
    REFERENCES `AFID`.`ubicaciones` (`id_ubicaciones`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`rol`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`rol` ;

CREATE TABLE IF NOT EXISTS `AFID`.`rol` (
  `nombre` ENUM('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR') NOT NULL,
  PRIMARY KEY (`nombre`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`rol_persona`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`rol_persona` ;

CREATE TABLE IF NOT EXISTS `AFID`.`rol_persona` (
  `personas_usuario` CHAR(64) NOT NULL,
  `rol_nombre` ENUM('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR') NOT NULL,
  PRIMARY KEY (`personas_usuario`, `rol_nombre`),
  INDEX `fk_personas_has_rol_rol1_idx` (`rol_nombre` ASC) VISIBLE,
  INDEX `fk_personas_has_rol_personas_idx` (`personas_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_personas_has_rol_personas`
    FOREIGN KEY (`personas_usuario`)
    REFERENCES `AFID`.`personas` (`usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_personas_has_rol_rol1`
    FOREIGN KEY (`rol_nombre`)
    REFERENCES `AFID`.`rol` (`nombre`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`funcionarios_en_sesion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`funcionarios_en_sesion` ;

CREATE TABLE IF NOT EXISTS `AFID`.`funcionarios_en_sesion` (
  `personas_usuario` CHAR(64) NOT NULL,
  `sesiones_id` INT NOT NULL,
  `profesor_encargado` ENUM('SI', 'NO') NOT NULL,
  PRIMARY KEY (`personas_usuario`, `sesiones_id`),
  INDEX `fk_personas_has_sesiones_sesiones1_idx` (`sesiones_id` ASC) VISIBLE,
  INDEX `fk_personas_has_sesiones_personas1_idx` (`personas_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_personas_has_sesiones_personas1`
    FOREIGN KEY (`personas_usuario`)
    REFERENCES `AFID`.`personas` (`usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_personas_has_sesiones_sesiones1`
    FOREIGN KEY (`sesiones_id`)
    REFERENCES `AFID`.`sesiones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`reservas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`reservas` ;

CREATE TABLE IF NOT EXISTS `AFID`.`reservas` (
  `sesiones_id` INT NOT NULL,
  `personas_usuario` VARCHAR(15) NOT NULL,
  `codigo` CHAR(6) NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_sesiones_has_personas_personas1_idx` (`personas_usuario` ASC) VISIBLE,
  INDEX `fk_sesiones_has_personas_sesiones1_idx` (`sesiones_id` ASC) VISIBLE,
  CONSTRAINT `fk_sesiones_has_personas_sesiones1`
    FOREIGN KEY (`sesiones_id`)
    REFERENCES `AFID`.`sesiones` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sesiones_has_personas_personas1`
    FOREIGN KEY (`personas_usuario`)
    REFERENCES `AFID`.`personas` (`usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`logs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`logs` ;

CREATE TABLE IF NOT EXISTS `AFID`.`logs` (
  `id_log` INT NOT NULL AUTO_INCREMENT,
  `operacion` ENUM('del', 'upd', 'ins', 'sel') NOT NULL,
  `tabla` VARCHAR(45) NOT NULL,
  `time_stamp` DATETIME NOT NULL,
  `personas_usuario` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`id_log`),
  INDEX `fk_logs_personas1_idx` (`personas_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_logs_personas1`
    FOREIGN KEY (`personas_usuario`)
    REFERENCES `AFID`.`personas` (`usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AFID`.`Penalizaciones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AFID`.`Penalizaciones` ;

CREATE TABLE IF NOT EXISTS `AFID`.`Penalizaciones` (
  `personas_usuario` VARCHAR(15) NOT NULL,
  `fin_penalizacion` DATETIME NOT NULL,
  INDEX `fk_Penalizaciones_personas1_idx` (`personas_usuario` ASC) VISIBLE,
  PRIMARY KEY (`personas_usuario`),
  CONSTRAINT `fk_Penalizaciones_personas1`
    FOREIGN KEY (`personas_usuario`)
    REFERENCES `AFID`.`personas` (`usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE USER IF NOT EXISTS 'atun_user'@'localhost' IDENTIFIED BY 'Admin01';
GRANT ALL PRIVILEGES ON afid.* TO 'atun_user'@'localhost';
