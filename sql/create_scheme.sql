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
  `especialidade` TEXT NULL,
  `cargo` TEXT NULL,
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

-- -----------------------------------------------------
-- VIEW `view_kpis`
-- -----------------------------------------------------

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `bd_cgpe`@`%` 
    SQL SECURITY DEFINER
VIEW `view_kpis` AS
    (SELECT 
        `A`.`id` AS `dummy`,
        `A`.`id` AS `id`,
        `A`.`startup` AS `startup`,
        `C`.`nome_projeto` AS `projeto`,
        `A`.`competencia` AS `competencia`,
        `A`.`tipo_kpi` AS `tipo_kpi`,
        `A`.`kpi` AS `kpi1`,
        `A`.`previsto` AS `previsto1`,
        `A`.`realizado` AS `realizado1`,
        `A`.`calculado` AS `calculado1`,
        `A`.`farol` AS `farol1`,
        `B`.`kpi` AS `kpi2`,
        `B`.`previsto` AS `previsto2`,
        `B`.`realizado` AS `realizado2`,
        `B`.`calculado` AS `calculado2`,
        `B`.`farol` AS `farol2`,
        `C`.`status` AS `status_projeto`
    FROM
        ((`indicadores` `A`
        JOIN `indicadores` `B`)
        JOIN `projetos` `C`)
    WHERE
        ((`A`.`kpi` < `B`.`kpi`)
            AND (`A`.`id` = `B`.`id`)
            AND (`A`.`competencia` = `B`.`competencia`)
            AND (`A`.`tipo_kpi` = `B`.`tipo_kpi`)
            AND (`A`.`id` = `C`.`id`)
            AND (UPPER(`C`.`status`) IN ('B - EM DESENVOLVIMENTO' , 'C - EM OPERAÇÃO'))
            AND (`A`.`in_carga` = 9)
            AND (`B`.`in_carga` = 9)
            AND (`C`.`in_carga` = 9))) UNION ALL (SELECT 
        COUNT(0) AS `dammy`,
        `A`.`id` AS `id`,
        `A`.`startup` AS `startup`,
        `C`.`nome_projeto` AS `projeto`,
        `A`.`competencia` AS `competencia`,
        `A`.`tipo_kpi` AS `tipo_kpi`,
        `A`.`kpi` AS `kpi1`,
        `A`.`previsto` AS `previsto1`,
        `A`.`realizado` AS `realizado1`,
        `A`.`calculado` AS `calculado1`,
        `A`.`farol` AS `farol1`,
        `B`.`kpi` AS `kpi2`,
        `B`.`previsto` AS `previsto2`,
        `B`.`realizado` AS `realizado2`,
        `B`.`calculado` AS `calculado2`,
        `B`.`farol` AS `farol2`,
        `C`.`status` AS `status_projeto`
    FROM
        ((`indicadores` `A`
        JOIN `indicadores` `B`)
        JOIN `projetos` `C`)
    WHERE
        ((`A`.`kpi` = `B`.`kpi`)
            AND (`A`.`id` = `B`.`id`)
            AND (`A`.`competencia` = `B`.`competencia`)
            AND (`A`.`tipo_kpi` = `B`.`tipo_kpi`)
            AND (`A`.`id` = `C`.`id`)
            AND (UPPER(`A`.`kpi`) = CONVERT( UPPER('Não Informado') USING UTF8))
            AND (UPPER(`C`.`status`) IN ('B - EM DESENVOLVIMENTO' , 'C - EM OPERAÇÃO'))
            AND (`A`.`in_carga` = 9)
            AND (`B`.`in_carga` = 9)
            AND (`C`.`in_carga` = 9))
    GROUP BY `A`.`id` , `A`.`startup` , `C`.`nome_projeto` , `A`.`competencia` , `A`.`tipo_kpi` , `A`.`kpi` , `A`.`previsto` , `A`.`realizado` , `A`.`calculado` , `A`.`farol` , `B`.`kpi` , `B`.`previsto` , `B`.`realizado` , `B`.`calculado` , `B`.`farol` , `C`.`status`
    HAVING (COUNT(0) > 1)) UNION ALL (SELECT 
        COUNT(0) AS `dammy`,
        `A`.`id` AS `id`,
        `A`.`startup` AS `startup`,
        `C`.`nome_projeto` AS `projeto`,
        `A`.`competencia` AS `competencia`,
        `A`.`tipo_kpi` AS `tipo_kpi`,
        `A`.`kpi` AS `kpi1`,
        `A`.`previsto` AS `previsto1`,
        `A`.`realizado` AS `realizado1`,
        `A`.`calculado` AS `calculado1`,
        `A`.`farol` AS `farol1`,
        `B`.`kpi` AS `kpi2`,
        `B`.`previsto` AS `previsto2`,
        `B`.`realizado` AS `realizado2`,
        `B`.`calculado` AS `calculado2`,
        `B`.`farol` AS `farol2`,
        `C`.`status` AS `status_projeto`
    FROM
        ((`indicadores` `A`
        JOIN `indicadores` `B`)
        JOIN `projetos` `C`)
    WHERE
        ((`A`.`kpi` = `B`.`kpi`)
            AND (`A`.`id` = `B`.`id`)
            AND (`A`.`competencia` = `B`.`competencia`)
            AND (`A`.`tipo_kpi` = `B`.`tipo_kpi`)
            AND (`A`.`id` = `C`.`id`)
            AND (UPPER(`A`.`kpi`) = CONVERT( UPPER('Não Informado') USING UTF8))
            AND (UPPER(`C`.`status`) IN ('B - EM DESENVOLVIMENTO' , 'C - EM OPERAÇÃO'))
            AND (`A`.`in_carga` = 9)
            AND (`B`.`in_carga` = 9)
            AND (`C`.`in_carga` = 9))
    GROUP BY `A`.`id` , `A`.`startup` , `C`.`nome_projeto` , `A`.`competencia` , `A`.`tipo_kpi` , `A`.`kpi` , `A`.`previsto` , `A`.`realizado` , `A`.`calculado` , `A`.`farol` , `B`.`kpi` , `B`.`previsto` , `B`.`realizado` , `B`.`calculado` , `B`.`farol` , `C`.`status`
    HAVING ((COUNT(0) = 1)
        AND (CONCAT(CAST(`A`.`previsto` AS CHAR CHARSET UTF8MB4),
            CAST(`A`.`realizado` AS CHAR CHARSET UTF8MB4)) < CONCAT(CAST(`B`.`previsto` AS CHAR CHARSET UTF8MB4),
            CAST(`B`.`realizado` AS CHAR CHARSET UTF8MB4))))) ORDER BY `startup` , `competencia` , `tipo_kpi` , `kpi1`;

