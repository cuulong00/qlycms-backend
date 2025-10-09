Aladding là một doanh nghiệp với 100 nhà hàng trên toàn quốc, phải nhập rất nhiều nguyên liệu, thực phẩm của nhiều nhà cung cấp khác nhau.  Định kì chúng tôi tạo ra các phiếu yêu cầu mua sắm và đảy cho tất cả các đối tác. Sau đó dựa vào phiếu yêu cầu mua sắm các đối tác sẽ bóc tách thành các phiếu giao hàng đến từng nhà hàng. Vào ngày cụ thể mà chúng tôi có yêu cầu trong pycms. Mọi việc hiện tại đang thực hiện thủ công .

Do việc quản lý các phiếu yêu cầu mua sắm thiện tại tại chưa được đồng nhất giữa các nhà cung cấp, dẫn đến việc quản lý gặp nhiều khó khăn. Vì quy cách đóng gói sản phẩm, đặt tên sản phẩm của các nhà cung cấp khác nhau là khác nhau, do đó chúng tôi gặp rất nhiều khó khăn trong việc đồng nhất được các dữ liệu này.  

Chúng tôi muốn xây dựng hệ thông quản lý yêu cầu mua sắm cho phép user của công ty tôi và user của đôi tác dễ dàng theo dõi phiếu yêu cầu mua sắp, đồng nhất được danh mục sản phẩm, đơn vị tính, giá sản phẩm hệ thống gồm 2 đối tượng user chính

1. User của tông ty (aladdin)
    1. Có thể nhìn được toàn bộ thông tin của phiếu yêu cầu mua sắm của tất cả các đối tác.
2. User của đối tác
    1. Chỉ nhìn được phiếu yêu cẩu mua sắm của công ty mình. Chỉ tạo được phiếu giao hàng cho công ty mình.
3. Phiếu yêu cầu mua sắm
            CREATE TABLE `orders` ( -- là phiếu yêu cầu mua sắm trong tài liệu hiện tại.
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
4. Phiếu giao hàng. 
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

5. Phiếu giao hàng chi tiết
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



5. Mối quan hệ giữa phiếu yêu cầu  mua sắm, và phiếu giao hàng
    1. 1 Phiếu yêu cầu mua sắm có thể tách thành nhiều phiếu giao hàng, vì phiếu yêu cầu mua sắp là kế hoạch chung cho nhiều nhà hàng gửi đến các nhà cung cấp, và phục vụ cho nhiều nhà hàng khác nhau. Do đó phía đối tác sẽ phải bóc tách các phiếu ycms này thành các phiếu giao hàng nhỏ, theo ngày, và theo nhà hàng (địa điểm giao đến)

Luồng chương trình như sau:

User Aladdin định kì tạo phiếu giao hàng, submit phiếu giao hàng lên hệ thống → Hệ thống sẽ gửi mail đến user nhà cung cấp, nhà cung cấp đăng nhập vào hệ thống kiểm tra phiếu ycms của mình → user nhà cung cấp cập nhật thông tin trên phiếu ycms → Tách thành các phiếu giao hàng.