<!doctype html>
<html lang="zh-cmn-Hans">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, shrink-to-fit=no" />
    <meta name="renderer" content="webkit" />
    <meta name="force-rendering" content="webkit" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

    <link href="https://cdn.bootcss.com/mdui/0.4.3/css/mdui.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/mdui/0.4.3/js/mdui.min.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <title>图书共享平台</title>
</head>

<body class="mdui-theme-primary-indigo mdui-theme-accent-pink mdui-appbar-with-toolbar mdui-drawer-body-left">
    <header class="mdui-appbar mdui-color-theme  mdui-appbar-fixed">
        <div class="mdui-toolbar mdui-color-theme">
            <a class="mdui-btn mdui-btn-icon" mdui-drawer="{target: '#sp-left-drawer'}"><i class="mdui-icon material-icons">menu</i></a>
            <a href="javascript:;" class="mdui-typo-headline">图书共享平台</a>
        </div>
    </header>
    <div class="mdui-drawer mdui-drawer-close" id="sp-left-drawer">
        <ul class="mdui-list">
            <a href="/index.php" class="mdui-list-item mdui-ripple">首页</a>
            <a href="/add.php" class="mdui-list-item mdui-ripple">赠送</a>
        </ul>
    </div>
    <div class="mdui-container sp-main-container mdui-center mdui-row" style="margin-top: 40px;">