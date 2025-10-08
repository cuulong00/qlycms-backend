/*
 Navicat Premium Dump SQL

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80406 (8.4.6)
 Source Host           : localhost:3306
 Source Schema         : xnt

 Target Server Type    : MySQL
 Target Server Version : 80406 (8.4.6)
 File Encoding         : 65001

 Date: 06/10/2025 13:31:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `department_id` int NOT NULL,
  `department_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'mã bộ phận của cơ sở',
  `oun_id` int NOT NULL,
  `process_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ware_house_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '0',
  `status_btt` tinyint NOT NULL DEFAULT '1',
  `created_by` int NOT NULL,
  `take_care` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `suggested_at` date NOT NULL,
  `delivery_term` date NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `fast_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `process_work_office` int DEFAULT NULL,
  `order_start_date` date DEFAULT NULL,
  `order_end_date` date DEFAULT NULL,
  `rate` tinyint NOT NULL DEFAULT '100',
  `inventory_id` bigint unsigned DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type_btt` tinyint NOT NULL DEFAULT '1' COMMENT '1: no btt, 2 is btt',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
