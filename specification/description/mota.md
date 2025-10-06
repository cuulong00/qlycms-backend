Aladding là một doanh nghiệp với 100 nhà hàng trên toàn quốc, phải nhập rất nhiều nguyên liệu, thực phẩm của nhiều nhà cung cấp khác nhau.  Định kì chúng tôi tạo ra các phiếu yêu cầu mua sắm và đảy cho tất cả các đối tác. Sau đó dựa vào phiếu yêu cầu mua sắm các đối tác sẽ bóc tách thành các phiếu giao hàng đến từng nhà hàng. Vào ngày cụ thể mà chúng tôi có yêu cầu trong pycms. Mọi việc hiện tại đang thực hiện thủ công .

Do việc quản lý các phiếu yêu cầu mua sắm thiện tại tại chưa được đồng nhất giữa các nhà cung cấp, dẫn đến việc quản lý gặp nhiều khó khăn. Vì quy cách đóng gói sản phẩm, đặt tên sản phẩm của các nhà cung cấp khác nhau là khác nhau, do đó chúng tôi gặp rất nhiều khó khăn trong việc đồng nhất được các dữ liệu này.  

Chúng tôi muốn xây dựng hệ thông quản lý yêu cầu mua sắm cho phép user của công ty tôi và user của đôi tác dễ dàng theo dõi phiếu yêu cầu mua sắp, đồng nhất được danh mục sản phẩm, đơn vị tính, giá sản phẩm hệ thống gồm 2 đối tượng user chính

1. User của tông ty (aladdin)
    1. Có thể nhìn được toàn bộ thông tin của phiếu yêu cầu mua sắm của tất cả các đối tác.
2. User của đối tác
    1. Chỉ nhìn được phiếu yêu cẩu mua sắm của công ty mình. Chỉ tạo được phiếu giao hàng cho công ty mình.
3. Phiếu yêu cầu mua sắm
    1. Gồm các trường : mã sản phẩm, tên sản phẩm, mã nhà cung cấp, đơn vị tính, mã nhà hàng, giá. ngày đề nghị, ngày muốn nhận, địa điểm giao, nhóm gật tư , số yêu cầu
4. Phiếu giao hàng. 
    1. Các trường của phiếu giao hàng gồm: STT, Tên sp, mã sp, địa điểm giao, Số lượng yêu cầu, SỐ lượng thực nhận, đơn vị tính, tổng tiền.
5. Mối quan hệ giữa phiếu yêu cầu  mua sắm, và phiếu giao hàng
    1. 1 Phiếu yêu cầu mua sắm có thể tách thành nhiều phiếu giao hàng, vì phiếu yêu cầu mua sắp là kế hoạch chung cho nhiều nhà hàng gửi đến các nhà cung cấp, và phục vụ cho nhiều nhà hàng khác nhau. Do đó phía đối tác sẽ phải bóc tách các phiếu ycms này thành các phiếu giao hàng nhỏ, theo ngày, và theo nhà hàng (địa điểm giao đến)

Luồng chương trình như sau:

User Aladdin định kì tạo phiếu giao hàng, submit phiếu giao hàng lên hệ thống → Hệ thống sẽ gửi mail đến user nhà cung cấp, nhà cung cấp đăng nhập vào hệ thống kiểm tra phiếu ycms của mình → user nhà cung cấp cập nhật thông tin trên phiếu ycms → Tách thành các phiếu giao hàng.