<?php
require_once 'data.php';
$id = $_GET['id'];
$regexResult = preg_match('/[^A-Za-z0-9_]/', $id);
if ($regexResult === false || $regexResult === 1) {
    die('Illegal character detected');
}
if (strlen($id) > 100) {
    die('Is this your id?');
}
// check if file exists
if (!file_exists('books/' . $id . '.info')) {
    die('Book not found');
}
$content = file_get_contents('books/' . $id . '.info');
$book = unserialize($content);
if (!($book instanceof Book) || !($book->reader instanceof Reader)) {
    throw new Exception('Invalid data');
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $book->title = $_POST['title'];
    $book->author = $_POST['author'];
    $book->summary = $_POST['summary'];
    file_put_contents('books/' . $book->id . '.info', waf(serialize($book)));
    $book->reader->setContent($_POST['content']);
}

function waf($data)
{
    return str_replace("'", "\\'", $data);
}

include_once 'common/header.php';
?>
<div class="mdui-card">
    <div class="mdui-card-primary">
        <div class="mdui-card-primary-title">修改图书</div>
    </div>
    <form method="post">
        <div class="mdui-card-content">
            <input type="hidden" name="id" value="<?php echo $_GET['id']; ?>" />
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">书名</label>
                <input class="mdui-textfield-input" type="text" value="<?php echo htmlspecialchars($book->title) ?>" name="title" required />
            </div>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">作者</label>
                <input class="mdui-textfield-input" type="text" name="author" value="<?php echo htmlspecialchars($book->author) ?>" required />
            </div>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">简介</label>
                <textarea class="mdui-textfield-input" name="summary"><?php echo htmlspecialchars($book->summary) ?></textarea>
            </div>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <label class="mdui-textfield-label">内容</label>
                <textarea class="mdui-textfield-input" name="content"><?php echo htmlspecialchars($book->reader->getContent()) ?></textarea>
        </div>
        <div class="mdui-card-actions">
            <button class="mdui-btn mdui-ripple mdui-color-theme-accent" type="submit">添加</button>
        </div>
    </form>
</div>