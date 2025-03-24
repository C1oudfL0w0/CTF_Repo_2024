<?php
include("./2024ISCC.php");
// 欢迎大家来到ISCC，本题大家将扮演《狂飙》中的警察，寻找关键证据，抓捕犯罪嫌疑人。
$code = file_get_contents(__FILE__);
highlight_string($code);

class police
{
    public $work;
    public $awarding = "salary";

    public function __construct($a)
    {
        $this ->work = $a;
    }
    
    public function __destruct()
    {
        echo "我是一名人民警察，打击违法犯罪义不容辞<br>";
        $this-> work = new suspect();
        echo $this-> work -> evidence_video;
        echo $this-> work -> evidence_fingerprint;
    }
}

class suspect
{
    private $video;
    private $fingerprint;

    public function __get($name)
    {
        if($name == "evidence_video")
        {
            echo "property.transactions怎么可能这么容易获得呢?<br>";
        }
        else
        {
            echo "blood.fingerprint怎么可能这么容易获得呢?<br>";
        }
    }

    public function __toString()
    {
        $this -> video = "property.transactions";
        $this -> fingerprint = "blood.fingerprint";
        return "差点就让你获得证据了<br>";
    }
}

class tools
{
    public $object;
    private $camera = 0;
    private $technology = 0;

    public function __construct()
    {
        echo "使用camera和technology可以找到蛛丝马迹<br>";
    }

    public function __invoke()
    {
        $this -> camera = 1;
        $this -> technology  = 1;
        echo $this->object;
    }
}

function filter($name)
{
    $safe = "evil";
    $name = str_replace($safe, "light", $name);
    return $name;
}

if (isset($_GET["evidence"]))
{
    $a = filter(serialize(new police($_GET["evidence"])));
    echo $a;
    global $tips;
    if((strpos($a, $tips) !== false) && unserialize($a) -> awarding == "pennant")
    {
        global $flag;
        echo $flag;
    }
}
?> 