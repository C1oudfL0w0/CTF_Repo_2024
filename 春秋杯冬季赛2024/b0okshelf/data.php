<?php

class Book {
    public $id;
    public $title;
    public $author;
    public $summary;
    public $reader;
}

class Reader
{
    public function __construct($location)
    {
        $this->location = $location;
    }
    private $location;
    public function getContent()
    {
        return file_get_contents($this->location);
    }
    public function setContent($content)
    {
        file_put_contents($this->location, $content);
    }
}
