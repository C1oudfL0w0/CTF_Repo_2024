<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_once 'data.php';
    $book = new Book();
    $book->id = uniqid();
    $book->title = $_POST['title'];
    $book->author = $_POST['author'];
    $book->summary = $_POST['summary'];
    $book->reader = new Reader('books/' . $book->id . '.txt');
    file_put_contents('books/' . $book->id . '.txt', '读书使人进步!');
    file_put_contents('books/' . $book->id . '.info', waf(serialize($book)));
    header('Location: index.php');
    exit();
}

function waf($data)
{
    return str_replace("'", "\\'", $data);
}

include_once 'common/header.php';
?>
<div class="mdui-card">
    <div class="mdui-card-primary">
        <div class="mdui-card-primary-title">添加图书</div>
    </div>
    <form method="post">
        <div class="mdui-card-content">
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">书名</label>
                <input class="mdui-textfield-input" type="text" name="title" required/>
            </div>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">作者</label>
                <input class="mdui-textfield-input" type="text" name="author" required/>
            </div>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">简介</label>
                <textarea class="mdui-textfield-input" name="summary" required></textarea>
            </div>
            内容: 读书使人进步
        </div>
        <div class="mdui-card-actions">
            <button class="mdui-btn mdui-ripple mdui-color-theme-accent" type="submit">添加</button>
        </div>
    </form>
</div>