const mysql = require("mysql");
const pg = require("pg"); // use pg@7.0.2

// WAF
const WAFWORDS = ["select", "union", "and", "or", "delete", "drop", "create", "alter", "truncate", "exec", 
                  "xp_cmdshell", "insert", "update", "sp_", "having", "exec master", "net user", "xp_", "waitfor", "information_schema", 
                  "table_schema", "sysobjects", "version", "group_concat", "concat", "distinct", "sysobjects", "user", "schema_name", "column_name", "table_name", 
                  "\", "/", "*", " ", ";", "--", "(", ")", "'", """, "=", "<", ">", "!=", "<>", 
"<=", ">=", "||", "+", "-", ",", ".", "[", "]", ":", "||", "*/", "/*", "_", "%"]

// debug: 
// ZnMucmVhZEZpbGUoJ3ByaW50RmxhZycsICd1dGY4JywgKGVyciwgZGF0YSkgPT4gew==
//     Y29uc29sZS5sb2coZGF0YSk7
// fSk7