<?php
include_once 'common/header.php';
include_once 'data.php';
$id = $_GET['id'];
// check if contains illegal characters
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
$bookContent = $book->reader->getContent();
?>

<div class="mdui-card">
    <div class="mdui-card-primary">
        <div class="mdui-card-primary-title"><?php echo $book->title; ?></div>
        <a href="update.php?id=<?php echo $id; ?>" class="mdui-btn mdui-btn-raised mdui-ripple mdui-color-theme-accent">编辑</a>
    </div>
    <div class="mdui-card-content">
        <p>作者: <?php echo $book->author; ?></p>
        <p>简介: <?php echo $book->summary; ?></p>
        <p><?php echo $bookContent; ?></p>
    </div>
</div>

<?php
include_once 'common/footer.php';
?>