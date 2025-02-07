// confirm-button.js
for (eve of ['htmx:afterSwap', 'DOMContentLoaded']) {
    document.addEventListener(eve, function () {
        let confirmLink = document.getElementById('confirmLink');
        if (confirmLink) {
            confirmLink.addEventListener('click', function (event) {
                event.preventDefault();
                Swal.fire({
                    title: 'تأكيد',
                    text: 'هل تريد تثبيت طلبك؟',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'نعم, ثبت الطلب',
                    confirmButtonColor: '#FE5656',
                    cancelButtonText: 'لا',
                    customClass: 'arabic-font p-2 h6'
                }).then((result) => {
                    if (result.isConfirmed) {
                        document.getElementById('ConfirmForm').submit();
                    }

                });
            });
        }
    });
}