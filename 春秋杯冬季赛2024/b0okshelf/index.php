<?php
include_once 'common/header.php';
function getBooks() {
    $books = array();
    $files = scandir('books');
    foreach ($files as $file) {
        if (substr($file, -5) === '.info') {
            $content = file_get_contents(dirname(__FILE__) . '/books/' . $file);
            $book = unserialize($content);
            $books[] = $book;
        }
    }
    return $books;
}
?>
<div class="mdui-card">
    <div class="mdui-card-primary">
        <div class="mdui-card-primary-title">图书列表</div>
    </div>
    <div class="mdui-card-content">
        <ul class="mdui-list">
            <?php
            include_once 'data.php';
            $books = getBooks();
            foreach ($books as $book) {
                echo '<a class="mdui-list-item mdui-ripple" href="view.php?id='.$book->id.'">';
                echo '<div class="mdui-list-item-avatar"><i class="mdui-icon material-icons">book</i></div>';
                echo '<div class="mdui-list-item-content">';
                echo '<div class="mdui-list-item-title">' . $book->title . '</div>';
                echo '<div class="mdui-list-item-text mdui-list-item-two-line">作者: ' . $book->author . '<br />简介: '.$book->summary.'</div>';
                echo '</div>';
                echo '</a>';
            }
            ?>
        </ul>
    </div>
</div>
<?php
include_once 'common/footer.php';
?>