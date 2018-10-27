// ヘッダーのアクティブ化

function activateNav(num)
{
    jQuery('.header__nav li:nth-child(' + num + ') a').addClass('active');
}
