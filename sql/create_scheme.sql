-- MySQL Script generated by MySQL Workbench
-- Thu Aug  5 18:34:04 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bd_cgpe
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bd_cgpe
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bd_cgpe` DEFAULT CHARACTER SET utf8 ;
USE `bd_cgpe` ;

-- -----------------------------------------------------
-- Table `Projetos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projetos` (
  `id` int NOT NULL,
  `startup` TEXT NOT NULL,
  `nome_projeto` TEXT NULL,
  `resumo` TEXT NULL,
  `lider_squad` TEXT NULL,
  `email_lider` TEXT NULL,
  `telefone_lider` TEXT NULL,
  `titular_cgpe` TEXT NULL,
  `substituto_cgpe` TEXT NULL,
  `observacao` TEXT NULL,
  `situacao` TEXT NULL,
  `status` TEXT NULL,
  `sigla_orgao` TEXT NULL,
  `in_carga` INT(1) NOT NULL,
  `dt_carga` DATETIME NOT NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Indicadores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `indicadores` (
  `id` int NOT NULL,
  `startup` TEXT NOT NULL,
  `competencia` DATE NOT NULL,
  `tipo_kpi` TEXT NOT NULL,
  `kpi` TEXT NOT NULL,
  `previsto` FLOAT NULL,
  `realizado` FLOAT NULL,
  `calculado` FLOAT NULL,
  `farol` INT(1) NULL,
  `in_carga` INT(1) NOT NULL,
  `dt_carga` DATETIME NOT NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Alocacoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `alocacoes` (
  `startup` TEXT NOT NULL,
  `nome` TEXT NOT NULL,
  `perfil` TEXT NULL,
  `origem` TEXT NULL,
  `cidade` TEXT NULL,
  `uf` TEXT(2) NULL,
  `observacao` TEXT NULL,
  `situacao` TEXT NULL,
  `sigla_orgao` TEXT NULL,
  `in_carga` INT(1) NOT NULL,
  `dt_carga` DATETIME NOT NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Relatos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `relatos` (
  `id` int NOT NULL,
  `startup` TEXT NOT NULL,
  `ultima_atualizacao` DATETIME NULL,
  `relato` TEXT NULL,
  `pontos_atencao` TEXT NULL,
  `in_carga` INT(1) NOT NULL,
  `dt_carga` DATETIME NOT NULL)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
