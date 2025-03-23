<?php
function filter($password){
    $filter_arr = array("admin","2024qwb");
    $filter = '/'.implode("|",$filter_arr).'/i';
    return preg_replace($filter,"nonono",$password);
}
class guest{
    public $username;
    public $value;
    public function __tostring(){
        if($this->username=="guest"){
            $value();
        }
        return $this->username;
    }
    public function __call($key,$value){
        if($this->username==md5($GLOBALS["flag"])){
            echo $GLOBALS["flag"];
        }
    }
}
class root{
    public $username;
    public $value;
    public function __get($key){
        if(strpos($this->username, "admin") == 0 && $this->value == "2024qwb"){
            $this->value = $GLOBALS["flag"];
            echo md5("hello:".$this->value);
        }
    }
}
class user{
    public $username;
    public $password;
    public $value;
    public function __invoke(){
        $this->username=md5($GLOBALS["flag"]);
        return $this->password->guess();
    }
    public function __destruct(){
        if(strpos($this->username, "admin") == 0 ){
            echo "hello".$this->username;
        }
    }
}
$user=unserialize(filter($_POST["password"]));
if(strpos($user->username, "admin") == 0 && $user->password == "2024qwb"){
    echo "hello!";
}