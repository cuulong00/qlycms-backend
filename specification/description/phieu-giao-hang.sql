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

 Date: 06/10/2025 14:00:12
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for receipt_details
-- ----------------------------


-- ----------------------------
-- Table structure for receipt_fast_details
-- ----------------------------
DROP TABLE IF EXISTS `receipt_fast_details`;
CREATE TABLE `receipt_fast_details` ( 
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `receipt_fast_id` int NOT NULL,
  `line_id` int NOT NULL,
  `line_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iit_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iit_uom` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_kho` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_bp` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ycms_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity_orders` double NOT NULL DEFAULT '0',
  `gia_nt` int NOT NULL DEFAULT '0',
  `tien_nt` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=246844 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for receipt_fasts
-- ----------------------------
DROP TABLE IF EXISTS `receipt_fasts`;
CREATE TABLE `receipt_fasts` ( 
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `receiving_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receiving_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receipt_date` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ma_kh` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ten_kh` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `t_tien` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receiving_detail` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16595 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for receipt_orders
-- ----------------------------
DROP TABLE IF EXISTS `receipt_orders`;
CREATE TABLE `receipt_orders` ( 
  `order_id` int unsigned NOT NULL,
  `receipt_id` int unsigned NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for receipts
-- ----------------------------
DROP TABLE IF EXISTS `receipts`;
CREATE TABLE `receipts` ( receipt_details receipt_fast_details  receipt_fasts  receipt_orders  
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `receipt_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiving_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiving_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `supplier_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `department_code` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `receipt_date` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_receipt` datetime DEFAULT NULL COMMENT 'ngày nhận',
  `status` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` tinyint NOT NULL DEFAULT '0' COMMENT '0: ycms, 1: not ycms',
  `status_office` tinyint NOT NULL DEFAULT '0',
  `fast_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `supplier_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `status_response` int DEFAULT NULL COMMENT '500, 400,...',
  `process_id` bigint unsigned DEFAULT NULL,
  `receipt_id_origin` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `receipts_receipt_id_unique` (`receipt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21137008 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `receipt_details`;
CREATE TABLE `receipt_details` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `receipt_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `receiving_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `line_id` int NOT NULL,
  `line_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iit_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `iit_code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `iit_uom` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ma_kho` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ycms_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantity_orders` double(8,4) NOT NULL,
  `quantity_approve` double(8,4) NOT NULL DEFAULT '0.0000',
  `price` int NOT NULL,
  `money` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receipt_details_receipt_id_index` (`receipt_id`),
  KEY `receipt_details_ycms_code_index` (`ycms_code`),
  KEY `receipt_details_iit_code_index` (`iit_code`)
) ENGINE=InnoDB AUTO_INCREMENT=358670 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;